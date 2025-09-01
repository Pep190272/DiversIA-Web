import Link from 'next/link';
import { EnvelopeIcon, PhoneIcon, MapPinIcon } from '@heroicons/react/24/outline';

export default function ContactoPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <Link href="/" className="text-blue-600 hover:text-blue-800 text-lg font-medium">
              ← DiversIA
            </Link>
            <nav className="flex space-x-8">
              <Link href="/registro" className="text-gray-700 hover:text-blue-600">
                Para Personas
              </Link>
              <Link href="/empresas" className="text-gray-700 hover:text-blue-600">
                Para Empresas
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            Ponte en Contacto con Nosotros
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            ¿Tienes preguntas sobre DiversIA? ¿Necesitas ayuda con tu proceso de inclusión laboral? 
            Estamos aquí para apoyarte en cada paso del camino.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Info */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-8">
                Información de Contacto
              </h2>
              
              <div className="space-y-6">
                <div className="flex items-start">
                  <EnvelopeIcon className="w-6 h-6 text-blue-600 mt-1 mr-4" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-1">Email</h3>
                    <p className="text-gray-600">contacto@diversia.com</p>
                    <p className="text-gray-600">info@diversia.com</p>
                  </div>
                </div>

                <div className="flex items-start">
                  <PhoneIcon className="w-6 h-6 text-blue-600 mt-1 mr-4" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-1">Teléfono</h3>
                    <p className="text-gray-600">+34 900 123 456</p>
                    <p className="text-sm text-gray-500">Lunes a Viernes, 9:00 - 18:00</p>
                  </div>
                </div>

                <div className="flex items-start">
                  <MapPinIcon className="w-6 h-6 text-blue-600 mt-1 mr-4" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-1">Oficina</h3>
                    <p className="text-gray-600">Calle Innovación, 123</p>
                    <p className="text-gray-600">28001 Madrid, España</p>
                  </div>
                </div>
              </div>

              {/* FAQ Quick Links */}
              <div className="mt-12">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Preguntas Frecuentes</h3>
                <div className="space-y-3">
                  <details className="bg-white p-4 rounded-lg shadow">
                    <summary className="font-medium cursor-pointer">¿Cómo funciona el proceso de matching?</summary>
                    <p className="mt-2 text-gray-600">
                      Nuestro algoritmo analiza tu perfil y fortalezas para conectarte con empresas 
                      que buscan exactamente tu tipo de talento neurodivergente.
                    </p>
                  </details>
                  
                  <details className="bg-white p-4 rounded-lg shadow">
                    <summary className="font-medium cursor-pointer">¿Es gratuito para personas neurodivergentes?</summary>
                    <p className="mt-2 text-gray-600">
                      Sí, todos nuestros servicios para personas neurodivergentes son completamente 
                      gratuitos. Las empresas pagan por acceder a nuestro talento.
                    </p>
                  </details>
                  
                  <details className="bg-white p-4 rounded-lg shadow">
                    <summary className="font-medium cursor-pointer">¿Qué tipos de trabajo ofrecen?</summary>
                    <p className="mt-2 text-gray-600">
                      Trabajamos con empresas de todos los sectores: tecnología, diseño, análisis de datos, 
                      atención al cliente, administración, y muchos más.
                    </p>
                  </details>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Envíanos un Mensaje
              </h2>
              
              <form className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Nombre *</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Tu nombre"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="form-label">Apellidos *</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Tus apellidos"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="form-label">Email *</label>
                  <input
                    type="email"
                    className="form-input"
                    placeholder="tu@email.com"
                    required
                  />
                </div>

                <div>
                  <label className="form-label">Teléfono</label>
                  <input
                    type="tel"
                    className="form-input"
                    placeholder="+34 600 000 000"
                  />
                </div>

                <div>
                  <label className="form-label">Tipo de Consulta *</label>
                  <select className="form-input" required>
                    <option value="">Selecciona una opción</option>
                    <option value="persona">Soy una persona neurodivergente</option>
                    <option value="empresa">Represento a una empresa</option>
                    <option value="asociacion">Soy de una asociación</option>
                    <option value="prensa">Consulta de prensa</option>
                    <option value="otro">Otro</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">Mensaje *</label>
                  <textarea
                    className="form-input"
                    rows={5}
                    placeholder="Cuéntanos en qué podemos ayudarte..."
                    required
                  />
                </div>

                <div className="flex items-start">
                  <input type="checkbox" className="mt-1 mr-2" required />
                  <span className="text-sm text-gray-600">
                    Acepto la{' '}
                    <Link href="/politica-privacidad" className="text-blue-600 hover:text-blue-800">
                      política de privacidad
                    </Link>{' '}
                    y el tratamiento de mis datos personales.
                  </span>
                </div>

                <button
                  type="submit"
                  className="w-full btn-primary text-lg py-3"
                >
                  Enviar Mensaje
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Support Section */}
      <section className="py-16 bg-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Otras Formas de Obtener Ayuda
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">📚</div>
              <h3 className="text-lg font-semibold mb-3">Centro de Ayuda</h3>
              <p className="text-gray-600 mb-4">
                Encuentra respuestas a las preguntas más comunes en nuestro centro de ayuda.
              </p>
              <button className="btn-secondary">
                Ver Artículos
              </button>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">💬</div>
              <h3 className="text-lg font-semibold mb-3">Chat en Vivo</h3>
              <p className="text-gray-600 mb-4">
                Chatea con nuestro equipo de soporte en tiempo real durante horario laboral.
              </p>
              <button className="btn-secondary">
                Iniciar Chat
              </button>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">👥</div>
              <h3 className="text-lg font-semibold mb-3">Comunidad</h3>
              <p className="text-gray-600 mb-4">
                Únete a nuestra comunidad online y conecta con otros miembros.
              </p>
              <Link href="/comunidad" className="btn-secondary inline-block">
                Unirse
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2025 DiversIA. Todos los derechos reservados.</p>
          <div className="mt-4 space-x-6">
            <Link href="/politica-privacidad" className="text-gray-400 hover:text-white">
              Política de Privacidad
            </Link>
            <Link href="/aviso-legal" className="text-gray-400 hover:text-white">
              Aviso Legal
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}