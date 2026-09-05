import type { MemberListResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined in environment variables.");
}

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

async function postRequest<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { method: 'POST' });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string; service: string }>("/health"),
  members: () => request<MemberListResponse>("/api/v1/members"),
  memberById: (id: string) => request<any>(`/api/v1/members/${id}`),
  reviewMember: (id: string) => postRequest<any>(`/api/v1/reviews/member?member_id=${id}`),
  reviewMemberGraph: (id: string) => postRequest<any>(`/api/v1/reviews/member-graph?member_id=${id}`),
  reviewMemberLLM: (id: string) => postRequest<any>(`/api/v1/reviews/member-llm?member_id=${id}`)
};

