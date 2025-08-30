import Link from 'next/link';
import { 
  BrainIcon, 
  LightBulbIcon, 
  UserGroupIcon, 
  ArrowRightIcon,
  CheckIcon 
} from '@heroicons/react/24/outline';

export default function PersonasNDPage() {
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
              <Link href="/empresas" className="text-gray-700 hover:text-blue-600">
                Para Empresas
              </Link>
              <Link href="/contacto" className="text-gray-700 hover:text-blue-600">
                Contacto
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-br from-purple-600 to-blue-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-6">
            Tu Neurodivergencia es tu <span className="text-yellow-300">Superpoder</span>
          </h1>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            TDAH, TEA, Dislexia, Altas Capacidades... Tu forma única de pensar es exactamente 
            lo que el mundo laboral necesita. Te ayudamos a encontrar el lugar perfecto para brillar.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/registro" 
              className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-3 px-8 rounded-lg transition-colors text-lg flex items-center justify-center gap-2"
            >
              Comenzar mi Test
              <ArrowRightIcon className="w-5 h-5" />
            </Link>
            <Link 
              href="#neurodivergencias" 
              className="bg-purple-500 hover:bg-purple-400 text-white font-bold py-3 px-8 rounded-lg transition-colors text-lg"
            >
              Conocer más
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            ¿Por qué DiversIA es Diferente?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white rounded-lg shadow">
              <BrainIcon className="w-16 h-16 mx-auto text-purple-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Entendemos tu Mente</h3>
              <p className="text-gray-600">
                Nuestros formularios están diseñados por psicólogos especializados en neurodivergencia. 
                No te juzgamos, te conocemos.
              </p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-lg shadow">
              <LightBulbIcon className="w-16 h-16 mx-auto text-purple-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Destacamos tus Fortalezas</h3>
              <p className="text-gray-600">
                Mientras otros ven limitaciones, nosotros vemos superpoderes. Tu perfil profesional 
                resalta lo que te hace excepcional.
              </p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-lg shadow">
              <UserGroupIcon className="w-16 h-16 mx-auto text-purple-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Empresas que te Valoran</h3>
              <p className="text-gray-600">
                Solo trabajamos con empresas que entienden el valor de la neurodiversidad y están 
                preparadas para recibirte.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Neurodivergencias Section */}
      <section id="neurodivergencias" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Formularios Especializados por Neurodivergencia
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* TDAH */}
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  ⚡
                </div>
                <h3 className="text-xl font-semibold ml-3">TDAH</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Formulario especializado para personas con TDAH que destaca tu creatividad, 
                capacidad de multitarea y pensamiento fuera de la caja.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Evaluación de niveles de atención</li>
                <li>• Identificación de fortalezas únicas</li>
                <li>• Adaptaciones recomendadas</li>
              </ul>
              <Link 
                href="/registro-tdah" 
                className="btn-primary w-full text-center"
              >
                Registro TDAH
              </Link>
            </div>

            {/* TEA */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  🧩
                </div>
                <h3 className="text-xl font-semibold ml-3">TEA</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Perfil específico para personas en el Espectro Autista que valora tu precisión, 
                pensamiento sistemático y atención al detalle.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Evaluación de comunicación</li>
                <li>• Sensibilidades y preferencias</li>
                <li>• Rutinas de trabajo óptimas</li>
              </ul>
              <Link 
                href="/registro-tea" 
                className="btn-primary w-full text-center"
              >
                Registro TEA
              </Link>
            </div>

            {/* Dislexia */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  📚
                </div>
                <h3 className="text-xl font-semibold ml-3">Dislexia</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Formulario adaptado para personas con dislexia que resalta tu creatividad, 
                pensamiento visual y habilidades de resolución de problemas.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Áreas de dificultad específicas</li>
                <li>• Herramientas de apoyo preferidas</li>
                <li>• Fortalezas compensatorias</li>
              </ul>
              <Link 
                href="/registro-dislexia" 
                className="btn-primary w-full text-center"
              >
                Registro Dislexia
              </Link>
            </div>

            {/* Discalculia */}
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  🔢
                </div>
                <h3 className="text-xl font-semibold ml-3">Discalculia</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Perfil que valora tus habilidades alternativas de procesamiento de información 
                y pensamiento no-numérico.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Fortalezas no-numéricas</li>
                <li>• Estrategias alternativas</li>
                <li>• Roles sin matemáticas complejas</li>
              </ul>
              <Link 
                href="/registro-discalculia" 
                className="btn-primary w-full text-center"
              >
                Registro Discalculia
              </Link>
            </div>

            {/* Altas Capacidades */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  🚀
                </div>
                <h3 className="text-xl font-semibold ml-3">Altas Capacidades</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Formulario para personas con altas capacidades que busca desafíos intelectuales 
                apropiados y entornos estimulantes.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Nivel de desafío deseado</li>
                <li>• Áreas de interés profundo</li>
                <li>• Necesidades intelectuales</li>
              </ul>
              <Link 
                href="/registro-altas-capacidades" 
                className="btn-primary w-full text-center"
              >
                Registro AA.CC.
              </Link>
            </div>

            {/* No estoy seguro */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gray-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  ❓
                </div>
                <h3 className="text-xl font-semibold ml-3">No estoy seguro/a</h3>
              </div>
              <p className="text-gray-600 mb-4">
                ¿No tienes diagnóstico o no estás seguro? Nuestro test general te ayudará 
                a identificar tus fortalezas únicas.
              </p>
              <ul className="text-sm text-gray-500 mb-4 space-y-1">
                <li>• Test de orientación inicial</li>
                <li>• Identificación de patrones</li>
                <li>• Recomendaciones personalizadas</li>
              </ul>
              <Link 
                href="/registro" 
                className="btn-primary w-full text-center"
              >
                Test General
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="py-16 bg-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Historias de Éxito
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-bold">M</span>
                </div>
                <div className="ml-3">
                  <h4 className="font-semibold">María - TDAH</h4>
                  <p className="text-sm text-gray-500">Desarrolladora Frontend</p>
                </div>
              </div>
              <p className="text-gray-600">
                "Gracias a DiversIA encontré una empresa que valora mi creatividad y mi capacidad 
                para resolver problemas de formas únicas. ¡Por fin trabajo sin esconder mi TDAH!"
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-bold">A</span>
                </div>
                <div className="ml-3">
                  <h4 className="font-semibold">Alejandro - TEA</h4>
                  <p className="text-sm text-gray-500">Analista de Datos</p>
                </div>
              </div>
              <p className="text-gray-600">
                "Mi atención al detalle y pensamiento sistemático son exactamente lo que necesitaba 
                mi nueva empresa. DiversIA me ayudó a encontrar el match perfecto."
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 font-bold">L</span>
                </div>
                <div className="ml-3">
                  <h4 className="font-semibold">Laura - Dislexia</h4>
                  <p className="text-sm text-gray-500">Diseñadora UX</p>
                </div>
              </div>
              <p className="text-gray-600">
                "Mi forma visual de pensar es mi mayor fortaleza como diseñadora. DiversIA me 
                conectó con una empresa que realmente entiende y aprovecha mi potencial."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Tu Camino hacia el Éxito Laboral
          </h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold text-xl">1</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Completa tu Test</h3>
              <p className="text-gray-600">
                Dedica 15-20 minutos a nuestro formulario especializado
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold text-xl">2</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Perfil Profesional</h3>
              <p className="text-gray-600">
                Creamos tu perfil destacando tus fortalezas únicas
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 font-bold text-xl">3</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Matching Inteligente</h3>
              <p className="text-gray-600">
                Te conectamos con empresas que buscan tu talento
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckIcon className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">¡A Trabajar!</h3>
              <p className="text-gray-600">
                Acompañamiento durante tu integración laboral
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-16 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">
            ¿Listo para Descubrir tu Potencial?
          </h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            Miles de personas neurodivergentes ya han encontrado su lugar ideal. 
            Tu próxima oportunidad laboral te está esperando.
          </p>
          <Link 
            href="/registro" 
            className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-4 px-8 rounded-lg transition-colors text-lg"
          >
            Comenzar mi Test Ahora
          </Link>
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