"""
Script para arreglar el template de Email Marketing añadiendo JavaScript
"""

def fix_template():
    """Arreglar el template añadiendo el script de JavaScript"""
    
    with open('email_marketing_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el final del primer template y añadir el script
    if 'function deleteAssociation(id)' not in content:
        # Añadir el script antes del cierre del primer template
        old_end = '''                </div>
            </div>
        </div>
    </div>
</body>
</html>
\'\'\''''
        
        new_end = '''                </div>
            </div>
        </div>
    </div>
    
    <script>
        function deleteAssociation(id) {
            if (confirm('¿Estás seguro de que quieres eliminar esta asociación?')) {
                fetch(`/email-marketing/delete/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error al eliminar: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Error de conexión: ' + error);
                });
            }
        }
    </script>
</body>
</html>
\'\'\''''
        
        # Solo reemplazar la primera ocurrencia (template de tabla)
        index = content.find(old_end)
        if index != -1:
            content = content[:index] + new_end + content[index + len(old_end):]
            
            with open('email_marketing_manager.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Template de Email Marketing arreglado con botones de eliminar")
        else:
            print("⚠️ No se encontró el patrón para reemplazar")
    else:
        print("✅ Script ya existe en el template")

if __name__ == "__main__":
    fix_template()