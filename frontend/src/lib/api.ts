/**
 * API Client for Alchemy Backend
 * Handles all HTTP communication with FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
    constructor(public status: number, message: string, public detail?: string) {
        super(message);
        this.name = 'ApiError';
    }
}

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new ApiError(response.status, error.error || 'Request failed', error.detail);
    }
    return response.json();
}

// ============================================================================
// Project API
// ============================================================================

export interface ProjectCreateRequest {
    idea: string;
}

export interface MessageSendRequest {
    project_id: string;
    content: string;
    mode: 'guided' | 'research' | 'update';
}

export interface OptionSelectRequest {
    project_id: string;
    message_id: string;
    option_id: string;
}

export interface CheckpointCreateRequest {
    project_id: string;
    label: string;
}

export interface CheckpointRevertRequest {
    project_id: string;
    checkpoint_id: string;
}

export interface ProjectResponse {
    project: any;
}

export interface MessageResponse {
    project: any;
    message: any;
}

export interface ArtifactsResponse {
    files: any[];
}

export interface CheckpointsResponse {
    checkpoints: any[];
}

export const api = {
    /**
     * Create a new project
     */
    async createProject(request: ProjectCreateRequest): Promise<ProjectResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<ProjectResponse>(response);
    },

    /**
     * List all projects
     */
    async listProjects(): Promise<{ projects: any[] }> {
        const response = await fetch(`${API_BASE_URL}/projects/`);
        return handleResponse<{ projects: any[] }>(response);
    },

    /**
     * Delete a project
     */
    async deleteProject(projectId: string): Promise<{ status: string }> {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE',
        });
        return handleResponse<{ status: string }>(response);
    },

    /**
     * Get project by ID
     */
    async getProject(projectId: string): Promise<ProjectResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`);
        return handleResponse<ProjectResponse>(response);
    },

    /**
     * Answer a roadmap question
     */
    async answerQuestion(request: any): Promise<ProjectResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<ProjectResponse>(response);
    },

    /**
     * Send a message to the AI
     */
    async sendMessage(request: MessageSendRequest): Promise<MessageResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<MessageResponse>(response);
    },

    /**
     * Select an option from an AI message
     */
    async selectOption(request: OptionSelectRequest): Promise<ProjectResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/option`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<ProjectResponse>(response);
    },

    /**
     * Create a checkpoint
     */
    async createCheckpoint(request: CheckpointCreateRequest): Promise<any> {
        const response = await fetch(`${API_BASE_URL}/projects/checkpoint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<any>(response);
    },

    /**
     * Revert to a checkpoint
     */
    async revertCheckpoint(request: CheckpointRevertRequest): Promise<ProjectResponse> {
        const response = await fetch(`${API_BASE_URL}/projects/revert`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request),
        });
        return handleResponse<ProjectResponse>(response);
    },

    /**
     * Get project artifacts
     */
    async getArtifacts(projectId: string) {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}/artifacts`);
        return handleResponse(response);
    },

    /**
     * Get project checkpoints
     */
    async getCheckpoints(projectId: string) {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}/checkpoints`);
        return handleResponse(response);
    },
};

export { ApiError };
