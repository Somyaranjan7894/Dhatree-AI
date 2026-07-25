import React from "react";
import { Modal, ModalProps } from "./Modal";

export type DialogProps = ModalProps;

/**
 * Dialog wraps Modal for semantic standard usage across Dhatree AI.
 */
export const Dialog: React.FC<DialogProps> = (props) => {
  return <Modal {...props} />;
};
