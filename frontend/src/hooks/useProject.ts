import { useState, useCallback, useEffect } from "react";
import { AIMode } from "@/components/alchemy/ModeSelector";
import { Message } from "@/components/alchemy/MessageCard";
import { Project } from "@/types/project";
import { api, ApiError } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

export function useProject() {
  const [project, setProject] = useState<Project | null>(null);
  const [recentProjects, setRecentProjects] = useState<any[]>([]);
  const [activeChatMode, setActiveChatMode] = useState<AIMode>("guided");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleApiError = useCallback((e: unknown) => {
    console.error("API Error:", e);
    const message = e instanceof ApiError ? e.message : "An unexpected error occurred";
    setError(message);
    toast({
      title: "Error",
      description: message,
      variant: "destructive",
    });
  }, [toast]);

  const refreshProjects = useCallback(async () => {
    try {
      const response = await api.listProjects();
      setRecentProjects(response.projects);
    } catch (e) {
      console.error("Failed to list projects:", e);
    }
  }, []);

  useEffect(() => {
    refreshProjects();
  }, [refreshProjects]);

  const loadProject = useCallback(async (projectId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.getProject(projectId);
      setProject(response.project);
      toast({
        title: "Project Loaded",
        description: `Switched to ${response.project.title}`,
      });
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [handleApiError, toast]);

  const removeProject = useCallback(async (projectId: string) => {
    try {
      await api.deleteProject(projectId);
      await refreshProjects();
      if (project?.id === projectId) {
        setProject(null);
      }
      toast({
        title: "Project Deleted",
        description: "The project has been removed successfully.",
      });
    } catch (e) {
      handleApiError(e);
    }
  }, [project, refreshProjects, handleApiError, toast]);

  const createProject = useCallback(async (idea: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.createProject({ idea });
      setProject(response.project);
      refreshProjects();
      toast({
        title: "Project Created",
        description: "Your architecture discovery journey has begun.",
      });
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [handleApiError, toast]);

  const sendMessage = useCallback(async (content: string, mode: AIMode) => {
    if (!project) return;

    setIsLoading(true);
    setError(null);
    // Optimistic user message update
    const userMessage: Message = {
      id: "temp-" + Date.now(),
      role: "user",
      content,
      timestamp: new Date(),
    };
    setProject(prev => prev ? { ...prev, messages: [...prev.messages, userMessage] } : null);

    try {
      const response = await api.sendMessage({
        project_id: project.id,
        content,
        mode
      });
      setProject(response.project);
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [project, handleApiError]);

  const answerQuestion = useCallback(async (questionId: string, answerIds: string[]) => {
    if (!project) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await api.answerQuestion({
        project_id: project.id,
        question_id: questionId,
        answer_ids: answerIds
      });
      setProject(response.project);
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [project, handleApiError]);

  const selectOption = useCallback(async (messageId: string, optionId: string) => {
    if (!project) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await api.selectOption({
        project_id: project.id,
        message_id: messageId,
        option_id: optionId
      });
      setProject(response.project);
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [project, handleApiError]);

  const useDefault = useCallback(async (messageId: string) => {
    const message = project?.messages.find(m => m.id === messageId);
    if (message?.options?.[0]) {
      await selectOption(messageId, message.options[0].id);
    } else if (project?.currentQuestion?.aiDefault) {
      // If it's a roadmap question with a default
      await answerQuestion(project.currentQuestion.id, [project.currentQuestion.aiDefault]);
    }
  }, [project, selectOption, answerQuestion]);

  const revertToId = useCallback(async (checkpointId: string) => {
    if (!project) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await api.revertCheckpoint({
        project_id: project.id,
        checkpoint_id: checkpointId
      });
      setProject(response.project);
      toast({
        title: "Checkpoint Restored",
        description: "Project state has been reverted.",
      });
    } catch (e) {
      handleApiError(e);
    } finally {
      setIsLoading(false);
    }
  }, [project, handleApiError, toast]);

  return {
    project,
    recentProjects,
    isLoading,
    error,
    createProject,
    loadProject,
    removeProject,
    sendMessage,
    answerQuestion,
    selectOption,
    useDefault,
    revertToCheckpoint: () => {
      if (project && project.checkpoints.length > 1) {
        const target = project.checkpoints[project.checkpoints.length - 2];
        revertToId(target.id);
      }
    },
    revertToId,
    closeProject: () => setProject(null),
    activeChatMode,
    setActiveChatMode
  };
}
