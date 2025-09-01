import Link from 'next/link';
import { BuildingOfficeIcon, UserGroupIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function EmpresasPage() {
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
              <Link href="/contacto" className="text-gray-700 hover:text-blue-600">
                Contacto
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-6">
            Encuentra Talento Neurodivergente Excepcional
          </h1>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            Las empresas más exitosas están descubriendo que la neurodiversidad no es solo inclusión, 
            es una ventaja competitiva. Conecta con profesionales únicos que aportan perspectivas innovadoras.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-lg transition-colors text-lg">
              Registrar Empresa
            </button>
            <button className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-3 px-8 rounded-lg transition-colors text-lg">
              Ver Demo
            </button>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            ¿Por qué elegir talento neurodivergente?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <ChartBarIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Mayor Productividad</h3>
              <p className="text-gray-600">
                Las personas neurodivergentes aportan enfoques únicos que incrementan la 
                eficiencia y la calidad del trabajo en un 30% promedio.
              </p>
            </div>
            <div className="text-center p-6">
              <UserGroupIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Diversidad de Pensamiento</h3>
              <p className="text-gray-600">
                Diferentes formas de procesar información llevan a soluciones más 
                creativas e innovadoras para desafíos complejos.
              </p>
            </div>
            <div className="text-center p-6">
              <BuildingOfficeIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Compromiso Excepcional</h3>
              <p className="text-gray-600">
                Mayor retención de empleados, menor ausentismo y un compromiso 
                extraordinario cuando encuentran el entorno adecuado.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Nuestros Servicios para Empresas
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gray-50 p-8 rounded-lg">
              <h3 className="text-2xl font-semibold mb-4">Reclutamiento Especializado</h3>
              <ul className="space-y-3 text-gray-600">
                <li>• Perfiles pre-evaluados y validados</li>
                <li>• Matching basado en fortalezas específicas</li>
                <li>• Proceso de selección adaptado</li>
                <li>• Seguimiento durante integración</li>
              </ul>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg">
              <h3 className="text-2xl font-semibold mb-4">Consultoría en Inclusión</h3>
              <ul className="space-y-3 text-gray-600">
                <li>• Auditoría de procesos actuales</li>
                <li>• Formación para equipos de RRHH</li>
                <li>• Adaptaciones del entorno laboral</li>
                <li>• Estrategias de retención</li>
              </ul>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg">
              <h3 className="text-2xl font-semibold mb-4">Formación y Sensibilización</h3>
              <ul className="space-y-3 text-gray-600">
                <li>• Talleres para managers y equipos</li>
                <li>• Guías de buenas prácticas</li>
                <li>• Recursos de comunicación</li>
                <li>• Certificación en neurodiversidad</li>
              </ul>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg">
              <h3 className="text-2xl font-semibold mb-4">Acompañamiento Continuo</h3>
              <ul className="space-y-3 text-gray-600">
                <li>• Mediación en casos complejos</li>
                <li>• Evaluaciones periódicas</li>
                <li>• Optimización de procesos</li>
                <li>• Reporting y métricas</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="py-16 bg-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Casos de Éxito
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h4 className="text-lg font-semibold mb-3">TechCorp</h4>
              <p className="text-gray-600 mb-4">
                "Incorporamos 15 desarrolladores neurodivergentes y nuestra productividad 
                en testing aumentó un 40%. Su atención al detalle es excepcional."
              </p>
              <p className="text-sm text-blue-600 font-medium">- Director de RRHH</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h4 className="text-lg font-semibold mb-3">InnovaDesign</h4>
              <p className="text-gray-600 mb-4">
                "Nuestro equipo de diseño es ahora más creativo e innovador. Las diferentes 
                perspectivas han revolucionado nuestros procesos creativos."
              </p>
              <p className="text-sm text-blue-600 font-medium">- CEO</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h4 className="text-lg font-semibold mb-3">DataAnalytics Pro</h4>
              <p className="text-gray-600 mb-4">
                "Contratamos analistas con TDAH y TEA. Su capacidad para detectar patrones 
                y anomalías en datos ha mejorado nuestros algoritmos significativamente."
              </p>
              <p className="text-sm text-blue-600 font-medium">- CTO</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">
            ¿Listo para Transformar tu Empresa?
          </h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            Únete a las empresas líderes que ya están aprovechando el poder de la neurodiversidad. 
            Comienza tu transformación hacia una organización más inclusiva e innovadora.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-colors text-lg">
              Comenzar Ahora
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-8 rounded-lg transition-colors text-lg">
              Solicitar Demo
            </button>
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
            <Link href="/contacto" className="text-gray-400 hover:text-white">
              Contacto
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}