import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Callable
from ai.utils.logger import ai_logger
from ai.models.model_manager import ModelManager

class BaseTrainer:
    """
    Reusable epoch-driven training execution framework.
    Handles device resolution, training loop, validation loop, early stopping,
    and learning-rate scheduling.
    """
    
    def __init__(self, model: nn.Module, 
                 train_loader: DataLoader, 
                 val_loader: DataLoader,
                 criterion: nn.Module,
                 optimizer: torch.optim.Optimizer,
                 model_manager: ModelManager,
                 model_name: str,
                 scheduler: torch.optim.lr_scheduler.LRScheduler = None,
                 use_gpu: bool = True,
                 patience: int = 5):
                 
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        ai_logger.info(f"Trainer initialized. Target device: {self.device}")
        
        self.model = model.to(self.device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.model_manager = model_manager
        self.model_name = model_name
        
        # Early stopping internals
        self.patience = patience
        self.best_val_loss = float('inf')
        self.epochs_without_improvement = 0
        
    def train_epoch(self) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, (inputs, targets) in enumerate(self.train_loader):
            inputs, targets = inputs.to(self.device), targets.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(self.train_loader)
        return avg_loss

    def validate_epoch(self, metric_func: Callable = None) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_targets = []
        
        with torch.no_grad():
            for inputs, targets in self.val_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                total_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                all_preds.extend(predicted.cpu().numpy())
                all_targets.extend(targets.cpu().numpy())
                
        avg_loss = total_loss / len(self.val_loader)
        metrics = {'val_loss': avg_loss}
        
        if metric_func:
            custom_metrics = metric_func(all_targets, all_preds)
            metrics.update(custom_metrics)
            
        return metrics

    def fit(self, epochs: int, metric_func: Callable = None):
        """
        Executes the full training loop across the specified number of epochs.
        """
        ai_logger.info(f"Starting training loop for {self.model_name} over {epochs} epochs.")
        
        for epoch in range(1, epochs + 1):
            train_loss = self.train_epoch()
            val_metrics = self.validate_epoch(metric_func=metric_func)
            val_loss = val_metrics['val_loss']
            
            ai_logger.info(f"Epoch {epoch}/{epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            
            if self.scheduler:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_loss)
                else:
                    self.scheduler.step()
            
            # Checkpoint and Early Stopping
            is_best = val_loss < self.best_val_loss
            if is_best:
                self.best_val_loss = val_loss
                self.epochs_without_improvement = 0
            else:
                self.epochs_without_improvement += 1
                
            self.model_manager.save_model(
                self.model, self.optimizer, epoch, val_metrics, self.model_name, is_best
            )
            
            if self.epochs_without_improvement >= self.patience:
                ai_logger.warning(f"Early stopping triggered after {epoch} epochs (Patience: {self.patience})")
                break
                
        ai_logger.info(f"Training complete. Best Val Loss: {self.best_val_loss:.4f}")
