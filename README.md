# ViceX Emulator

**ViceX Emulator** es un proyecto experimental de escritorio para Windows, dedicado a organizar y analizar una carpeta de GTA VI.

> Proyecto independiente y no oficial. No está afiliado a Rockstar Games ni a Microsoft.
> Esta primera versión es solamente un lanzador/analizador: **no emula Xbox ni garantiza que GTA VI pueda ejecutarse**.

## Funciones de esta primera versión

- Interfaz de escritorio con tema oscuro y acentos morados.
- Selección de la carpeta del juego.
- Análisis local de archivos y detección de ejecutables conocidos.
- Campo para localizar una compilación local de VIctory.
- No ejecuta automáticamente archivos del juego ni descarga DLLs.

## Requisitos

- Windows 10/11 de 64 bits.
- Python 3.10 o superior.
- Dependencias de `requirements.txt`.

## Ejecutar desde el código

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\main.py
```

## Seguridad

Usa únicamente archivos que tengas derecho a utilizar. No desactives Microsoft Defender ni ejecutes juegos o herramientas desconocidas como administrador. La opción de iniciar el juego está deshabilitada en esta versión hasta verificar la compatibilidad real del motor.

## Estado

- [x] Estructura inicial del repositorio
- [x] Interfaz gráfica base
- [x] Selector de carpeta
- [x] Análisis básico de archivos
- [ ] Integración segura con VIctory
- [ ] Pruebas de compatibilidad
- [ ] Empaquetado como `.exe`
