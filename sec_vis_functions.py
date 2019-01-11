import rhinoscriptsyntax
import System.Windows.Forms

def GetFolder(folder=None, message=None, title=None):
    """Display browse-for-folder dialog allowing the user to select a folder
    Parameters:
      folder[opt] = a default folder
      message[opt] = a prompt or message
      title[opt] = a dialog box title
    Returns:
      selected folder
      None on error
    """
    dlg = System.Windows.Forms.FolderBrowserDialog()
    if folder:
        if not isinstance(folder, str): folder = str(folder)
        dlg.SelectedPath = folder
    if message:
        if not isinstance(message, str): message = str(message)
        dlg.Description = message
    if dlg.ShowDialog()==System.Windows.Forms.DialogResult.OK:
        return dlg.SelectedPath
    return dlg.SelectedPath

print(Browse())
