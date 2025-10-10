from pathlib import Path
from datetime import datetime as dt


class Tools:
	@staticmethod
	def project_root() -> Path:
		"""Returns the root directory of the project."""
		return Path(__file__).parent.parent

	@staticmethod
	def files_dir(nested_directory: str = None, filename: str = None) -> Path:
		"""Returns the path to the 'Files' directory, optionally appending a nested directory and/or filename."""
		files_path = Tools.project_root() / 'files'
		if nested_directory:
			files_path = files_path / nested_directory
		files_path.mkdir(parents=True, exist_ok=True)

		if filename:
			return files_path / filename
		return files_path

	@staticmethod
	def timestamp() -> str:
		"""Returns the current timestamp formatted as 'YYYY-MM-DD_HH-MM-SS'."""
		return dt.now().strftime("%Y-%m-%d_%H-%M-%S")
