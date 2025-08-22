
TAREAS_LISTADO_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Tareas - DiversIA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .task-card { transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; }
        .task-card:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .status-badge { font-size: 0.75rem; font-weight: 600; }
        .status-completado { background-color: #d4edda !important; color: #155724; }
        .status-en-progreso { background-color: #d1ecf1 !important; color: #0c5460; }
        .status-pendiente { background-color: #fff3cd !important; color: #856404; }
        .edit-form { display: none; } .task-content { display: block; }
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2>📋 Gestión de Tareas - DiversIA</h2>
                    <div>
                        <span class="badge bg-info me-2">{{ total_tareas }} tareas</span>
                        <a href="/sistema-gestion" class="btn btn-outline-secondary me-2">← Sistema</a>
                        <a href="/diversia-admin-logout" class="btn btn-outline-danger">Salir</a>
                    </div>
                </div>
                
                <div class="row g-3">
                    {% for tarea in tareas %}
                    <div class="col-lg-6 col-xl-4">
                        <div class="card task-card h-100" id="card-{{ tarea.id }}">
                            <div class="card-body">
                                <div class="task-content" id="content-{{ tarea.id }}">
                                    <div class="d-flex justify-content-between align-items-start mb-3">
                                        <h6 class="card-title mb-0 text-primary">Tarea #{{ tarea.id }}</h6>
                                        <span class="badge status-badge status-{{ tarea.estado.lower().replace(' \', \'-\') }}">{{ tarea.estado }}</span>
                                    </div>
                                    <h5 class="card-subtitle mb-3">{{ tarea.tarea[:80] }}{% if tarea.tarea|length > 80 %}...{% endif %}</h5>
                                    <div class="mb-2">
                                        <small class="text-muted">👤 Colaborador:</small>
                                        <div>{{ tarea.colaborador or "Sin asignar" }}</div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-6">
                                            <small class="text-muted">📅 Inicio:</small>
                                            <div>{{ tarea.fecha_inicio or "-" }}</div>
                                        </div>
                                        <div class="col-6">
                                            <small class="text-muted">⏰ Final:</small>
                                            <div>{{ tarea.fecha_final or "-" }}</div>
                                        </div>
                                    </div>
                                    {% if tarea.notas %}
                                    <div class="mt-3">
                                        <small class="text-muted">📝 Notas:</small>
                                        <div class="small">{{ tarea.notas[:100] }}{% if tarea.notas|length > 100 %}...{% endif %}</div>
                                    </div>
                                    {% endif %}
                                    <div class="mt-3 text-end">
                                        <button class="btn btn-sm btn-primary" onclick="editTask({{ tarea.id }})">✏️ Editar</button>
                                    </div>
                                </div>
                                
                                <div class="edit-form" id="edit-{{ tarea.id }}">
                                    <form onsubmit="saveTask(event, {{ tarea.id }})">
                                        <div class="mb-3">
                                            <label class="form-label">Descripción de la Tarea</label>
                                            <textarea class="form-control" name="tarea" rows="3" required>{{ tarea.tarea }}</textarea>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Colaborador Asignado</label>
                                            <input type="text" class="form-control" name="colaborador" value="{{ tarea.colaborador or "" }}">
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-6">
                                                <label class="form-label">Fecha Inicio</label>
                                                <input type="date" class="form-control" name="fecha_inicio" value="{{ tarea.fecha_inicio or "" }}">
                                            </div>
                                            <div class="col-6">
                                                <label class="form-label">Fecha Final</label>
                                                <input type="date" class="form-control" name="fecha_final" value="{{ tarea.fecha_final or "" }}">
                                            </div>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Estado</label>
                                            <select class="form-control" name="estado" required>
                                                <option value="Pendiente" {{ "selected" if tarea.estado == "Pendiente" else "" }}>Pendiente</option>
                                                <option value="En progreso" {{ "selected" if tarea.estado == "En progreso" else "" }}>En progreso</option>
                                                <option value="Completado" {{ "selected" if tarea.estado == "Completado" else "" }}>Completado</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Notas</label>
                                            <textarea class="form-control" name="notas" rows="3">{{ tarea.notas or "" }}</textarea>
                                        </div>
                                        <div class="d-flex gap-2">
                                            <button type="submit" class="btn btn-success">💾 Guardar</button>
                                            <button type="button" class="btn btn-secondary" onclick="cancelEdit({{ tarea.id }})">❌ Cancelar</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% if not tareas %}
                <div class="text-center mt-5">
                    <h4>No hay tareas registradas</h4>
                    <p class="text-muted">Las tareas están restauradas desde los respaldos.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    <script>
        function editTask(id) {
            document.getElementById("content-" + id).style.display = "none";
            document.getElementById("edit-" + id).style.display = "block";
        }
        function cancelEdit(id) {
            document.getElementById("content-" + id).style.display = "block";
            document.getElementById("edit-" + id).style.display = "none";
        }
        function saveTask(event, id) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            fetch("/tareas/update/" + id, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert("✅ Tarea actualizada correctamente");
                    location.reload();
                } else {
                    alert("❌ Error: " + result.error);
                }
            })
            .catch(error => alert("❌ Error de conexión: " + error));
        }
    </script>
</body>
</html>
"""
