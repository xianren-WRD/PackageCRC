## 功能描述

1. 此程序首先会计算所选的二进制(bin)文件的CRC32校验值(小端)，并在所选文件的同一路径下创建一个名为"_UpgradeFileOutput"的目录。

2. 随后，在"_UpgradeFileOutput"目录下，程序会创建一个与所选的bin文件同名的bin文件，并将原始数据拷贝到该文件中，然后追加写入CRC32计算结果。

3. 最后，在"_UpgradeFileOutput"目录下，程序会创建一个与所选的bin文件同名的hex文件，然后加载上述新建的bin文件的数据，将数据转换后写入其中。

请注意，此程序不会修改所选的原始bin文件。

## 使用示例

请点击文件选择按钮，选择一个bin文件，并在输入框中输入起始地址，最后点击转换按钮即可。

## 说明

1. 资源文件存放在"resources"目录中，目前该目录仅包含按钮图标文件。
2. 如果选择文件后没有输入起始地址，直接点击转换按钮，则默认起始地址为：0x10000。
3. pyinstaller打包后在win7无法运行，提示缺少api-ms-win-core-path-l1-1-0.dll。因为python3.9不再支持win7，所以如果目标计算机是win7系统，可以使用python3.8和对应的PyInstaller来打包解决这个问题。

## 打包依赖

在运行打包命令之前，请确保已经满足以下依赖：

- Python 3.8 或其他版本
- PyInstaller 工具（路径：C:\Python38\Scripts\pyinstaller.exe）

## 打包命令

使用以下命令将 `PackageCRC.py` 文件打包成一个独立的可执行文件：

`C:\Python38\Scripts\pyinstaller.exe --onefile --noconsole --icon=..\resources\arrow_location_icon.ico PackageCRC.py`

请确保替换路径中的 `C:\Python38\Scripts\pyinstaller.exe` 为你实际的 `pyinstaller` 工具路径。

- `--onefile`: 生成单个可执行文件，而不是一堆依赖文件。
- `--noconsole`: 不显示命令行窗口。
- `--icon=..\resources\arrow_location_icon.ico`: 使用指定的图标文件作为可执行文件的图标。
- `PackageCRC.py`: 要打包的 Python 脚本文件。

## 打包结果

运行打包命令后，将在当前工作目录生成一个名为 `dist` 的文件夹。在该文件夹中，你将找到打包好的可执行文件 `PackageCRC.exe`。

## 运行打包文件

要运行打包好的可执行文件，只需双击 `PackageCRC.exe` 文件即可。将"resources"文件夹和`PackageCRC.exe`置于同一路径下，按钮即可正确显示图标，否则显示默认样式图标。


