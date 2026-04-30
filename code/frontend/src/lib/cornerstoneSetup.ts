import { init as csInit } from "@cornerstonejs/core";
import {
  init as csToolsInit,
  addTool,
  ToolGroupManager,
  PanTool,
  ZoomTool,
  WindowLevelTool,
  LengthTool,
  BrushTool,
  Enums as csToolsEnums,
} from "@cornerstonejs/tools";
import { init as dicomImageLoaderInit } from "@cornerstonejs/dicom-image-loader";

let initialized = false;

export async function initCornerstone() {
  if (initialized) return;
  await csInit();
  await csToolsInit();
  dicomImageLoaderInit({ maxWebWorkers: 1 });

  addTool(PanTool);
  addTool(ZoomTool);
  addTool(WindowLevelTool);
  addTool(LengthTool);
  addTool(BrushTool);

  initialized = true;
}

export const TOOL_GROUP_ID = "carotis-tools";

export function createDefaultToolGroup() {
  const group = ToolGroupManager.createToolGroup(TOOL_GROUP_ID);
  if (!group) return ToolGroupManager.getToolGroup(TOOL_GROUP_ID)!;
  group.addTool(PanTool.toolName);
  group.addTool(ZoomTool.toolName);
  group.addTool(WindowLevelTool.toolName);
  group.addTool(LengthTool.toolName);
  group.addTool(BrushTool.toolName);
  group.setToolActive(PanTool.toolName, {
    bindings: [{ mouseButton: csToolsEnums.MouseBindings.Auxiliary }],
  });
  group.setToolActive(WindowLevelTool.toolName, {
    bindings: [{ mouseButton: csToolsEnums.MouseBindings.Primary }],
  });
  group.setToolActive(ZoomTool.toolName, {
    bindings: [{ mouseButton: csToolsEnums.MouseBindings.Secondary }],
  });
  return group;
}
