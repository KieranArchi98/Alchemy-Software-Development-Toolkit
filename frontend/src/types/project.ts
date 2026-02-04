import { AIMode } from "@/components/alchemy/ModeSelector";
import { SpecSection } from "@/components/alchemy/SpecificationView";
import { ProjectFile } from "@/components/alchemy/FileCarousel";
import { Message } from "@/components/alchemy/MessageCard";

export interface ProjectState {
    purpose: string;
    constraints: string[];
    app_archetype: string;
    features: string[];
    data_model: any;
    frontend_design: any;
    backend_design: any;
    ai_usage: any;
    non_functional_requirements: string[];
}

export interface Checkpoint {
    id: string;
    timestamp: string;
    label: string;
    state: ProjectState;
    progress: number;
}

export interface Project {
    id: string;
    title: string;
    idea: string;
    progress: number;
    lastSaved: string | null;
    activePhase: string;
    activeChatMode: AIMode;
    state?: ProjectState;
    spec?: any; // CanonicalProjectSpec
    sections: SpecSection[]; // Derived from state for UI
    files: ProjectFile[];     // Generated artifacts
    messages: Message[];
    checkpoints: Checkpoint[];
    currentQuestion?: any;
}

export const INITIAL_PROJECT_STATE: ProjectState = {
    purpose: "",
    constraints: [],
    app_archetype: "",
    features: [],
    data_model: null,
    frontend_design: null,
    backend_design: null,
    ai_usage: null,
    non_functional_requirements: [],
};
