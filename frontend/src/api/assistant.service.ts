import { apiClient } from './client';

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at?: string;
}

export interface ChatSession {
  id: string;
  provider_name: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface SendMessageResponse {
  session_id: string;
  message: string;
  created_at: string;
}

export const assistantService = {
  getSessions: async (): Promise<ChatSession[]> => {
    const response = await apiClient.get('/assistant/');
    const res = response as any;
    return res.data || res;
  },

  getSession: async (id: string): Promise<ChatSession> => {
    const response = await apiClient.get(`/assistant/${id}/`);
    const res = response as any;
    return res.data || res;
  },

  sendMessage: async (message: string, sessionId?: string): Promise<SendMessageResponse> => {
    const response = await apiClient.post('/assistant/chat/', {
      message,
      session_id: sessionId
    });
    const res = response as any;
    return res.data || res;
  }
};
