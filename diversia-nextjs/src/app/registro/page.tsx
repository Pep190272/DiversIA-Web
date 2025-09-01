import RegistroForm from '@/components/RegistroForm';
import Link from 'next/link';

export default function RegistroPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="text-blue-600 hover:text-blue-800 text-lg font-medium">
            ← Volver al inicio
          </Link>
        </div>

        {/* Intro */}
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Descubre tu Potencial Profesional
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Nuestro test especializado te ayudará a identificar tus fortalezas y crear un perfil 
            profesional adaptado a tus necesidades. ¡Es el primer paso hacia tu inclusión laboral!
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 inline-block">
            <p className="text-blue-800">
              ⏱️ <strong>Tiempo estimado:</strong> 10-15 minutos<br/>
              🔒 <strong>Confidencial:</strong> Tus datos están seguros<br/>
              ✨ <strong>Personalizado:</strong> Adaptado a personas neurodivergentes
            </p>
          </div>
        </div>

        {/* Formulario */}
        <RegistroForm />

        {/* Info adicional */}
        <div className="max-w-2xl mx-auto mt-12 text-center">
          <h3 className="text-xl font-semibold mb-4">¿Qué sucede después?</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-2xl mb-2">📊</div>
              <h4 className="font-medium mb-2">Análisis Personalizado</h4>
              <p className="text-sm text-gray-600">
                Analizamos tu perfil y fortalezas
              </p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-2xl mb-2">🎯</div>
              <h4 className="font-medium mb-2">Match con Empresas</h4>
              <p className="text-sm text-gray-600">
                Te conectamos con oportunidades
              </p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-2xl mb-2">🚀</div>
              <h4 className="font-medium mb-2">Acompañamiento</h4>
              <p className="text-sm text-gray-600">
                Te apoyamos en tu proceso
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}