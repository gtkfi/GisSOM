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
        /// <summary>
        /// Dialog to select file to open from file system
        /// </summary>
        /// <param name="initialPath"></param>
        /// <param name="filter"></param>
        /// <param name="checkFileExists"></param>
        /// <param name="checkPathExists"></param>
        /// <returns></returns>
        string OpenFileDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true);

        /// <summary>
        /// Dialog for saving a file in windows file system
        /// </summary>
        /// <param name="initialPath"></param>
        /// <param name="filter"></param>
        /// <param name="checkFileExists"></param>
        /// <param name="checkPathExists"></param>
        /// <param name="fileName"></param>
        /// <returns></returns>
        string SaveFileDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true, string fileName="");

        /// <summary>
        /// Dialog for selecting multiple files from file system
        /// </summary>
        /// <param name="initialPath"></param>
        /// <param name="filter"></param>
        /// <param name="checkFileExists"></param>
        /// <param name="checkPathExists"></param>
        /// <returns></returns>
        List<string> OpenFilesDialog(string initialPath = "", string filter = "", bool checkFileExists = true, bool checkPathExists = true);

        /// <summary>
        /// Display notification message on screen
        /// </summary>
        /// <param name="message"></param>
        /// <param name="notificationType"></param>
        void ShowNotification(string message, string notificationType);

        /// <summary>
        /// Dialog for selecting a folder from file system
        /// </summary>
        /// <param name="selectedPath"></param>
        /// <param name="rootFolder"></param>
        /// <returns></returns>
        string SelectFolderDialog(string selectedPath = "", Environment.SpecialFolder rootFolder = Environment.SpecialFolder.MyComputer);

        /// <summary>
        /// Show message dialog
        /// </summary>
        void ShowMessageDialog();
    }
}
