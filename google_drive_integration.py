"""
Google Drive Integration for DiversIA
Gestión segura de documentos, CVs y certificados
"""

import os
import io
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Google Drive APIs
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import fitz  # PyMuPDF para extraer texto de PDFs
from PIL import Image
import docx2txt  # Para archivos Word

logger = logging.getLogger(__name__)

class GoogleDriveManager:
    """
    Gestor seguro de Google Drive para documentos de DiversIA
    """
    
    def __init__(self):
        self.setup_credentials()
        self.setup_folder_structure()
        
    def setup_credentials(self):
        """Configurar credenciales seguras de Google Drive"""
        try:
            # Cargar credenciales desde variable de entorno
            credentials_json = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
            if not credentials_json:
                logger.warning("Google Drive credentials not found")
                self.service = None
                return
            
            # Parsear JSON de credenciales
            credentials_info = json.loads(credentials_json)
            
            # Scopes necesarios para Drive
            scopes = [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file'
            ]
            
            # Crear credenciales
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=scopes
            )
            
            # Inicializar servicio
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("✅ Google Drive service initialized")
            
        except Exception as e:
            logger.error(f"Error setting up Google Drive: {e}")
            self.service = None
    
    def setup_folder_structure(self):
        """Crear estructura de carpetas en Drive"""
        if not self.service:
            return
            
        self.folders = {
            'root': 'DiversIA_Documents',
            'cvs': 'CVs_Candidatos',
            'certificates': 'Certificados',
            'evaluations': 'Evaluaciones_Neurodivergencia',
            'company_docs': 'Documentos_Empresas',
            'reports': 'Reportes_Sistema'
        }
        
        # Crear carpetas si no existen
        try:
            for folder_name, folder_title in self.folders.items():
                folder_id = self.get_or_create_folder(folder_title)
                self.folders[folder_name] = folder_id
                
        except Exception as e:
            logger.error(f"Error creating folder structure: {e}")
    
    def get_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Obtener o crear carpeta en Drive"""
        try:
            # Buscar carpeta existente
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(q=query).execute()
            files = results.get('files', [])
            
            if files:
                return files[0]['id']
            
            # Crear nueva carpeta
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                folder_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(body=folder_metadata).execute()
            logger.info(f"Created folder: {folder_name}")
            return folder.get('id')
            
        except Exception as e:
            logger.error(f"Error managing folder {folder_name}: {e}")
            return None
    
    def upload_candidate_cv(self, file_path: str, candidate_id: str, metadata: Dict) -> Dict[str, Any]:
        """Subir CV de candidato con metadatos"""
        try:
            if not self.service:
                return {'error': 'Google Drive not configured'}
            
            # Metadatos del archivo
            file_name = f"CV_{candidate_id}_{datetime.now().strftime('%Y%m%d')}"
            
            file_metadata = {
                'name': file_name,
                'parents': [self.folders['cvs']],
                'description': json.dumps({
                    'candidate_id': candidate_id,
                    'upload_date': datetime.now().isoformat(),
                    'type': 'cv',
                    'metadata': metadata
                })
            }
            
            # Subir archivo
            media = MediaFileUpload(file_path)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Extraer texto del CV
            extracted_text = self.extract_text_from_file(file_path)
            
            result = {
                'file_id': file.get('id'),
                'file_name': file.get('name'),
                'web_link': file.get('webViewLink'),
                'extracted_text': extracted_text,
                'upload_success': True
            }
            
            logger.info(f"CV uploaded successfully: {file_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error uploading CV: {e}")
            return {'error': str(e), 'upload_success': False}
    
    def upload_certificate(self, file_path: str, candidate_id: str, cert_type: str, metadata: Dict) -> Dict[str, Any]:
        """Subir certificado de neurodivergencia"""
        try:
            if not self.service:
                return {'error': 'Google Drive not configured'}
            
            file_name = f"CERT_{cert_type}_{candidate_id}_{datetime.now().strftime('%Y%m%d')}"
            
            file_metadata = {
                'name': file_name,
                'parents': [self.folders['certificates']],
                'description': json.dumps({
                    'candidate_id': candidate_id,
                    'certificate_type': cert_type,
                    'upload_date': datetime.now().isoformat(),
                    'metadata': metadata
                })
            }
            
            media = MediaFileUpload(file_path)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            result = {
                'file_id': file.get('id'),
                'file_name': file.get('name'),
                'web_link': file.get('webViewLink'),
                'certificate_type': cert_type,
                'upload_success': True
            }
            
            logger.info(f"Certificate uploaded: {file_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error uploading certificate: {e}")
            return {'error': str(e), 'upload_success': False}
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extraer texto de diferentes tipos de archivo"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self.extract_text_from_docx(file_path)
            elif file_extension in ['.txt']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logger.warning(f"Unsupported file type: {file_extension}")
                return ""
                
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extraer texto de PDF usando PyMuPDF"""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extraer texto de Word"""
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {e}")
            return ""
    
    def search_candidate_documents(self, candidate_id: str) -> List[Dict]:
        """Buscar todos los documentos de un candidato"""
        try:
            if not self.service:
                return []
            
            # Buscar en todas las carpetas relevantes
            folders_to_search = [self.folders['cvs'], self.folders['certificates'], self.folders['evaluations']]
            documents = []
            
            for folder_id in folders_to_search:
                query = f"'{folder_id}' in parents"
                results = self.service.files().list(q=query).execute()
                files = results.get('files', [])
                
                for file in files:
                    # Verificar si el archivo pertenece al candidato
                    if candidate_id in file.get('name', ''):
                        documents.append({
                            'file_id': file['id'],
                            'name': file['name'],
                            'created_time': file.get('createdTime'),
                            'size': file.get('size'),
                            'web_link': file.get('webViewLink')
                        })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def generate_candidate_report(self, candidate_id: str, data: Dict) -> Dict[str, Any]:
        """Generar reporte completo del candidato"""
        try:
            if not self.service:
                return {'error': 'Google Drive not configured'}
            
            # Crear contenido del reporte
            report_content = self.create_report_content(candidate_id, data)
            
            # Crear archivo temporal
            temp_file = f"/tmp/report_{candidate_id}.html"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # Subir a Drive
            file_name = f"Reporte_{candidate_id}_{datetime.now().strftime('%Y%m%d_%H%M')}"
            
            file_metadata = {
                'name': file_name,
                'parents': [self.folders['reports']],
                'description': f"Reporte completo del candidato {candidate_id}"
            }
            
            media = MediaFileUpload(temp_file, mimetype='text/html')
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Limpiar archivo temporal
            os.remove(temp_file)
            
            return {
                'file_id': file.get('id'),
                'file_name': file.get('name'),
                'web_link': file.get('webViewLink'),
                'report_success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {'error': str(e), 'report_success': False}
    
    def create_report_content(self, candidate_id: str, data: Dict) -> str:
        """Crear contenido HTML del reporte"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte DiversIA - Candidato {candidate_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Candidato DiversIA</h1>
                <p><strong>ID:</strong> {candidate_id}</p>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            
            <div class="section">
                <h2>Información del Perfil</h2>
                <p><strong>Tipo de Neurodivergencia:</strong> {data.get('tipo_neurodivergencia', 'No especificado')}</p>
                <p><strong>Experiencia:</strong> {data.get('experiencia_anos', 0)} años</p>
                <p><strong>Nivel Educativo:</strong> {data.get('nivel_educativo', 'No especificado')}</p>
            </div>
            
            <div class="section">
                <h2>Métricas de Matching</h2>
                <div class="metric">
                    <strong>Compatibilidad Promedio:</strong> {data.get('avg_compatibility', 0):.1f}%
                </div>
                <div class="metric">
                    <strong>Matches Exitosos:</strong> {data.get('successful_matches', 0)}
                </div>
                <div class="metric">
                    <strong>Entrevistas Realizadas:</strong> {data.get('interviews', 0)}
                </div>
            </div>
            
            <div class="section">
                <h2>Documentos Asociados</h2>
                <ul>
        """
        
        # Agregar lista de documentos
        documents = data.get('documents', [])
        for doc in documents:
            html_content += f"<li>{doc.get('name', 'Documento')} - {doc.get('created_time', 'Fecha desconocida')}</li>"
        
        html_content += """
                </ul>
            </div>
            
            <div class="section">
                <h2>Recomendaciones</h2>
                <p>Basado en el análisis de datos, se recomienda:</p>
                <ul>
                    <li>Continuar con el proceso de matching automático</li>
                    <li>Revisar adaptaciones específicas necesarias</li>
                    <li>Mantener actualizado el perfil profesional</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de almacenamiento"""
        try:
            if not self.service:
                return {'error': 'Google Drive not configured'}
            
            stats = {}
            
            for folder_name, folder_id in self.folders.items():
                if isinstance(folder_id, str):
                    query = f"'{folder_id}' in parents"
                    results = self.service.files().list(q=query).execute()
                    files = results.get('files', [])
                    
                    total_size = 0
                    for file in files:
                        size = file.get('size')
                        if size:
                            total_size += int(size)
                    
                    stats[folder_name] = {
                        'file_count': len(files),
                        'total_size_mb': total_size / (1024 * 1024)
                    }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return {'error': str(e)}

# Instancia global del gestor
drive_manager = GoogleDriveManager()

def upload_candidate_document(file_path: str, candidate_id: str, doc_type: str, metadata: Dict = None) -> Dict:
    """
    Función de conveniencia para subir documentos de candidatos
    """
    if not metadata:
        metadata = {}
    
    if doc_type == 'cv':
        return drive_manager.upload_candidate_cv(file_path, candidate_id, metadata)
    elif doc_type == 'certificate':
        cert_type = metadata.get('certificate_type', 'general')
        return drive_manager.upload_certificate(file_path, candidate_id, cert_type, metadata)
    else:
        logger.error(f"Unknown document type: {doc_type}")
        return {'error': 'Unknown document type'}

if __name__ == "__main__":
    # Test del sistema
    stats = drive_manager.get_storage_stats()
    print("Storage Stats:", json.dumps(stats, indent=2, ensure_ascii=False))