import { AppShell } from "@/components/alchemy/AppShell";
import { Landing } from "@/components/alchemy/Landing";
import { Workspace } from "@/components/alchemy/Workspace";
import { useProject } from "@/hooks/useProject";

const Index = () => {
  const {
    project,
    recentProjects,
    isLoading,
    error,
    createProject,
    loadProject,
    removeProject,
    sendMessage,
    selectOption,
    useDefault,
    revertToCheckpoint,
    closeProject,
  } = useProject();

  return (
    <AppShell>
      {project ? (
        <Workspace
          project={project}
          isLoading={isLoading}
          onSendMessage={sendMessage}
          onSelectOption={selectOption}
          onUseDefault={useDefault}
          onRevert={revertToCheckpoint}
          onBack={closeProject}
        />
      ) : (
        <Landing
          onCreateProject={createProject}
          onLoadProject={loadProject}
          onDeleteProject={removeProject}
          isLoading={isLoading}
          recentProjects={recentProjects}
        />
      )}
    </AppShell>
  );
};

export default Index;
