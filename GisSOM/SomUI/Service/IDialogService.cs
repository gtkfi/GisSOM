using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SomUI.Service
{
    /// <summary>
    /// Level of the notification
    /// </summary>
    public enum NotificationLevel
    {
        Information = 0,
        Good = 1,
        Warning = 2,
        Error = 3
    }
    /// <summary>
    /// IDialog Service.
    /// </summary>
    public interface IDialogService
    {
        string OpenFileDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true);
        string SaveFileDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true, string fileName="");
        List<string> OpenFilesDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true);
        //void ShowNotification(string message, NotificationLevel level, Action callbackAction = null, int timeout = 5);
        void ShowNotification(string message, string notificationType);
        string SelectFolderDialog(string selectedPath = "", Environment.SpecialFolder rootFolder = Environment.SpecialFolder.MyComputer);
        void ShowMessageDialog();
    }
}
