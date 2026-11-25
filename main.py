import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFrame, QHBoxLayout, QLabel, QMainWindow,
    QMessageBox, QPushButton, QVBoxLayout, QWidget
)


APP_STYLE = """
QMainWindow, QWidget { background: #080812; color: #f4f1ff; font-family: Segoe UI; }
QLabel#muted { color: #aaa4c4; }
QLabel#brand { color: #ffffff; font-size: 25px; font-weight: 800; }
QLabel#hero { color: #ffffff; font-size: 32px; font-weight: 800; }
QFrame#panel { background: #141326; border: 1px solid #6736c9; border-radius: 18px; }
QPushButton {
  background: #211638; color: white; border: 1px solid #a34cff;
  border-radius: 12px; padding: 13px 18px; font-size: 14px; font-weight: 700;
}
QPushButton:hover { background: #38205d; border: 1px solid #d18aff; }
QPushButton:disabled { color: #77718b; background: #191725; border-color: #383247; }
QPushButton#play {
  background: #5720b8; border: 2px solid #c477ff; font-size: 20px; padding: 16px;
}
QPushButton#play:disabled { background: #211b2e; border-color: #4b405d; }
"""


class ViceXWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ViceX Emulator")
        self.resize(1120, 700)
        self.game_dir: Path | None = None

        central = QWidget()
        self.setCentralWidget(central)
        page = QVBoxLayout(central)
        page.setContentsMargins(34, 24, 34, 20)
        page.setSpacing(18)

        header = QHBoxLayout()
        brand = QLabel("♛ ViceX <span style='color:#c05cff'>EMULATOR</span>")
        brand.setObjectName("brand")
        header.addWidget(brand)
        header.addStretch()
        for label in ("INICIO", "CONFIGURACIÓN", "ACERCA DE"):
            tab = QLabel(label)
            tab.setStyleSheet("color:#d8caff; font-weight:700; padding:10px 14px;")
            header.addWidget(tab)
        page.addLayout(header)

        hero = QLabel("TU BIBLIOTECA. UN SOLO JUEGO.")
        hero.setObjectName("hero")
        page.addWidget(hero)
        subtitle = QLabel("ViceX es un lanzador experimental dedicado a GTA VI.")
        subtitle.setObjectName("muted")
        page.addWidget(subtitle)

        body = QHBoxLayout()
        body.setSpacing(22)

        game_card = QFrame()
        game_card.setObjectName("panel")
        game_layout = QVBoxLayout(game_card)
        game_layout.setContentsMargins(24, 24, 24, 24)
        game_layout.setSpacing(14)

        cover = QLabel("GTA\nVI")
        cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cover.setMinimumSize(300, 310)
        cover.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            "stop:0 #251044, stop:0.5 #7126a8, stop:1 #f04e9a);"
            "border-radius:14px; color:white; font-size:64px; font-weight:900;"
        )
        game_layout.addWidget(cover)
        game_name = QLabel("GRAND THEFT AUTO VI")
        game_name.setStyleSheet("font-size:18px; font-weight:800;")
        game_layout.addWidget(game_name)
        game_note = QLabel("Juego exclusivo configurado para este lanzador.")
        game_note.setObjectName("muted")
        game_layout.addWidget(game_note)

        controls = QFrame()
        controls.setObjectName("panel")
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(24, 24, 24, 24)
        controls_layout.setSpacing(16)

        section = QLabel("PREPARAR JUEGO")
        section.setStyleSheet("font-size:20px; font-weight:800; color:#d7a4ff;")
        controls_layout.addWidget(section)
        self.folder_label = QLabel("Selecciona la carpeta donde tienes los archivos de GTA VI.")
        self.folder_label.setWordWrap(True)
        self.folder_label.setObjectName("muted")
        controls_layout.addWidget(self.folder_label)

        choose_btn = QPushButton("📁  SELECCIONAR CARPETA")
        choose_btn.clicked.connect(self.choose_folder)
        controls_layout.addWidget(choose_btn)

        self.scan_btn = QPushButton("🔎  ANALIZAR ARCHIVOS")
        self.scan_btn.clicked.connect(self.scan_folder)
        self.scan_btn.setEnabled(False)
        controls_layout.addWidget(self.scan_btn)

        self.status = QLabel("Estado: esperando una carpeta.")
        self.status.setWordWrap(True)
        self.status.setStyleSheet("color:#c9b8e8; padding:10px;")
        controls_layout.addWidget(self.status)

        self.report = QLabel("")
        self.report.setWordWrap(True)
        self.report.setObjectName("muted")
        controls_layout.addWidget(self.report)

        self.play_btn = QPushButton("▶  JUGAR")
        self.play_btn.setObjectName("play")
        self.play_btn.setEnabled(False)
        self.play_btn.setToolTip("Se habilitará cuando exista una ruta de ejecución compatible y verificada.")
        controls_layout.addWidget(self.play_btn)

        warning = QLabel("La ejecución está desactivada: VIctory aún debe demostrar compatibilidad real.")
        warning.setWordWrap(True)
        warning.setStyleSheet("color:#ffcf83; font-size:12px;")
        controls_layout.addWidget(warning)
        controls_layout.addStretch()

        body.addWidget(game_card, 1)
        body.addWidget(controls, 1)
        page.addLayout(body, 1)

        footer = QHBoxLayout()
        footer.addWidget(QLabel("ENTER  Seleccionar"))
        footer.addWidget(QLabel("ESC  Atrás"))
        footer.addWidget(QLabel("TAB  Menú"))
        footer.addStretch()
        footer.addWidget(QLabel("ViceX Emulator  •  Experimental"))
        for i in range(footer.count()):
            item = footer.itemAt(i)
            if item and item.widget():
                item.widget().setStyleSheet(
                    "color:#b8a8d5; background:#11101d; padding:9px 12px;"
                    "border:1px solid #44305e; border-radius:8px;"
                )
        page.addLayout(footer)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de GTA VI")
        if not folder:
            return
        self.game_dir = Path(folder)
        self.folder_label.setText(str(self.game_dir))
        self.scan_btn.setEnabled(True)
        self.report.setText("")
        self.status.setText("Estado: carpeta seleccionada. Analiza los archivos para continuar.")

    def scan_folder(self):
        if not self.game_dir or not self.game_dir.is_dir():
            QMessageBox.warning(self, "ViceX", "Selecciona una carpeta válida.")
            return

        files = list(self.game_dir.iterdir())
        exe_names = [p.name for p in files if p.is_file() and p.suffix.lower() == ".exe"]
        known_xbox_exe = self.game_dir / "game_scarlett_master.exe"

        lines = [
            f"Elementos en la carpeta principal: {len(files)}",
            f"Ejecutables .exe encontrados: {len(exe_names)}",
        ]
        if exe_names:
            lines.append("Ejecutables: " + ", ".join(exe_names[:8]))
        if known_xbox_exe.exists():
            lines.append("Detectado: game_scarlett_master.exe (formato asociado a una compilación Xbox).")
            lines.append("Esto no confirma que pueda ejecutarse en Windows.")
        else:
            lines.append("No se encontró game_scarlett_master.exe en la raíz.")
        self.report.setText("\n".join(lines))
        self.status.setText("Análisis básico completado. No se ha ejecutado ningún archivo.")
        self.play_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = ViceXWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
