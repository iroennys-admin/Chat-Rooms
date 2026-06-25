<div align="center">
  <img src="https://img.icons8.com/fluency/96/chat.png" width="80" />
  <h1>ChatRooms</h1>
  <p>Salas de chat con Django</p>
</div>

---

App web para crear salas de chat por temas. Cada sala tiene su propio chat, los usuarios se pueden unir y dejar mensajes.

## Lo que hace

- Crear salas con un nombre, tema y descripción
- Mandar mensajes dentro de cada sala
- Unirte a las salas que te interesen
- Buscar salas por nombre o filtrar por tema
- Perfil de usuario con sus salas y actividad
- Registro, login y logout

## Inicio rápido

```bash
git clone https://github.com/iroennys-admin/Chat-Rooms.git
cd Chat-Rooms
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Tecnologías

- Django 6.0
- SQLite
- CSS vanilla con tema oscuro

## Modelos

- **Topic** — temas para agrupar salas
- **Room** — salas de chat, cada una con su tema y participantes
- **Message** — mensajes dentro de las salas
