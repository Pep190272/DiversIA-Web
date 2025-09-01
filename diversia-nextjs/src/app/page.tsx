import Link from 'next/link';
import { ArrowRightIcon, UserGroupIcon, BuildingOfficeIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-blue-600">DiversIA</h1>
              <span className="ml-2 text-sm text-gray-600">Inclusión Laboral</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <Link href="/personas-nd" className="text-gray-700 hover:text-blue-600 transition-colors">
                Personas ND
              </Link>
              <Link href="/empresas" className="text-gray-700 hover:text-blue-600 transition-colors">
                Empresas
              </Link>
              <Link href="/comunidad" className="text-gray-700 hover:text-blue-600 transition-colors">
                Comunidad
              </Link>
              <Link href="/contacto" className="text-gray-700 hover:text-blue-600 transition-colors">
                Contacto
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main>
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-5xl font-bold text-gray-900 mb-6">
              Conectamos talento <span className="text-blue-600">neurodivergente</span> con empresas inclusivas
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              DiversIA es la plataforma líder que facilita la inclusión laboral de personas con TDAH, TEA, Dislexia y otras neurodivergencias.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/registro" 
                className="btn-primary flex items-center justify-center gap-2 text-lg px-8 py-4"
              >
                Haz mi test
                <ArrowRightIcon className="w-5 h-5" />
              </Link>
              <Link 
                href="/empresas" 
                className="btn-secondary flex items-center justify-center gap-2 text-lg px-8 py-4"
              >
                Soy empresa
                <BuildingOfficeIcon className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
              ¿Cómo funciona DiversIA?
            </h3>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <UserGroupIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                <h4 className="text-xl font-semibold mb-3">Para Personas Neurodivergentes</h4>
                <p className="text-gray-600">
                  Completa nuestro test especializado y crea tu perfil profesional adaptado a tus fortalezas y necesidades.
                </p>
              </div>
              <div className="text-center p-6">
                <BuildingOfficeIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                <h4 className="text-xl font-semibold mb-3">Para Empresas</h4>
                <p className="text-gray-600">
                  Conecta con talento diverso y aprende a crear ambientes de trabajo verdaderamente inclusivos.
                </p>
              </div>
              <div className="text-center p-6">
                <AcademicCapIcon className="w-16 h-16 mx-auto text-blue-600 mb-4" />
                <h4 className="text-xl font-semibold mb-3">Formación y Apoyo</h4>
                <p className="text-gray-600">
                  Accede a recursos, formación especializada y una comunidad de apoyo para maximizar el éxito laboral.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-blue-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h3 className="text-3xl font-bold text-white mb-6">
              ¿Listo para comenzar tu camino hacia la inclusión laboral?
            </h3>
            <p className="text-xl text-blue-100 mb-8">
              Únete a miles de personas que ya han encontrado su lugar en el mundo laboral.
            </p>
            <Link 
              href="/registro" 
              className="bg-white text-blue-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-lg transition-colors text-lg"
            >
              Comenzar ahora
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h5 className="text-lg font-semibold mb-4">DiversIA</h5>
              <p className="text-gray-400">
                Conectamos talento neurodivergente con empresas inclusivas.
              </p>
            </div>
            <div>
              <h5 className="text-lg font-semibold mb-4">Para Personas</h5>
              <ul className="space-y-2">
                <li><Link href="/personas-nd" className="text-gray-400 hover:text-white">Personas ND</Link></li>
                <li><Link href="/registro" className="text-gray-400 hover:text-white">Haz mi test</Link></li>
                <li><Link href="/registro-tdah" className="text-gray-400 hover:text-white">Registro TDAH</Link></li>
                <li><Link href="/registro-tea" className="text-gray-400 hover:text-white">Registro TEA</Link></li>
              </ul>
            </div>
            <div>
              <h5 className="text-lg font-semibold mb-4">Para Empresas</h5>
              <ul className="space-y-2">
                <li><Link href="/empresas" className="text-gray-400 hover:text-white">Registro Empresas</Link></li>
                <li><Link href="/asociaciones" className="text-gray-400 hover:text-white">Asociaciones</Link></li>
              </ul>
            </div>
            <div>
              <h5 className="text-lg font-semibold mb-4">Legal</h5>
              <ul className="space-y-2">
                <li><Link href="/politica-privacidad" className="text-gray-400 hover:text-white">Política de Privacidad</Link></li>
                <li><Link href="/aviso-legal" className="text-gray-400 hover:text-white">Aviso Legal</Link></li>
                <li><Link href="/contacto" className="text-gray-400 hover:text-white">Contacto</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 DiversIA. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}