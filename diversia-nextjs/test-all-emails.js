/**
 * Test de todos los formularios con emails automáticos
 * Este script probará que todos los formularios envíen emails correctamente
 */

const API_BASE = 'http://localhost:5000/api';

// Datos de prueba para cada formulario
const testData = {
  registro: {
    nombre: 'María',
    apellidos: 'García López',
    email: 'test.diversia.registro@gmail.com',
    telefono: '555-0123',
    ciudad: 'Madrid',
    fecha_nacimiento: '1995-05-15',
    tipo_neurodivergencia: 'TDAH',
    diagnostico_formal: true,
    habilidades: 'Programación, análisis de datos',
    experiencia_laboral: '3 años en desarrollo web',
    formacion_academica: 'Ingeniería Informática',
    intereses_laborales: 'Desarrollo frontend, UX/UI',
    adaptaciones_necesarias: 'Horarios flexibles',
    motivaciones: 'Busco un ambiente inclusivo'
  },
  
  'registro-tdah': {
    nombre: 'Carlos',
    apellidos: 'Ruiz Martín',
    email: 'test.diversia.tdah@gmail.com',
    telefono: '555-0124',
    ciudad: 'Barcelona',
    fecha_nacimiento: '1992-08-20',
    diagnostico_formal: true,
    habilidades: 'Creatividad, resolución de problemas',
    experiencia_laboral: '5 años en marketing digital',
    formacion_academica: 'Licenciatura en Marketing',
    intereses_laborales: 'Marketing creativo, estrategia digital',
    adaptaciones_necesarias: 'Espacios sin distracciones',
    motivaciones: 'Quiero usar mi creatividad al máximo',
    tipo_tdah: 'Combinado',
    nivel_atencion: 'Medio',
    impulsividad: 'Alto',
    hiperactividad: 'Medio',
    medicacion: 'Sí, metilfenidato'
  },

  'registro-empresa': {
    nombre_empresa: 'TechInclusiva SL',
    email_contacto: 'test.diversia.empresa@gmail.com',
    telefono: '555-0125',
    ciudad: 'Valencia',
    sector: 'Tecnología',
    tamano_empresa: '50-200 empleados',
    sitio_web: 'https://techinclusiva.es',
    descripcion_empresa: 'Empresa tecnológica comprometida con la diversidad',
    politicas_inclusion: 'Tenemos políticas específicas para neurodiversidad'
  },

  'registro-asociacion': {
    nombre_asociacion: 'Asociación TDAH Valencia',
    acronimo: 'ATDAHV',
    pais: 'España',
    ciudad: 'Valencia',
    email: 'test.diversia.asociacion@gmail.com',
    telefono: '555-0126',
    sitio_web: 'https://tdahvalencia.org',
    descripcion: 'Asociación de apoyo a personas con TDAH en Valencia',
    contacto_nombre: 'Ana Fernández',
    contacto_cargo: 'Presidenta',
    neurodivergencias_atendidas: ['TDAH', 'TEA'],
    servicios: ['Apoyo psicológico', 'Talleres educativos']
  }
};

// Función para hacer petición POST
async function testEndpoint(endpoint, data) {
  console.log(`\n🧪 Probando ${endpoint}...`);
  
  try {
    const response = await fetch(`${API_BASE}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    
    if (response.ok && result.success) {
      console.log(`✅ ${endpoint}: ${result.message}`);
      return true;
    } else {
      console.log(`❌ ${endpoint}: Error - ${result.error || 'Unknown error'}`);
      if (result.details) {
        console.log('   Detalles:', result.details);
      }
      return false;
    }
  } catch (error) {
    console.log(`❌ ${endpoint}: Error de conexión - ${error.message}`);
    return false;
  }
}

// Función para probar todos los formularios
async function testAllForms() {
  console.log('🚀 Iniciando pruebas de todos los formularios con emails...\n');
  console.log('📧 Los emails se enviarán a: diversiaeternals@gmail.com');
  console.log('🔔 También se enviarán emails de bienvenida a cada usuario/empresa/asociación');
  
  const results = [];
  
  // Probar cada endpoint
  for (const [endpoint, data] of Object.entries(testData)) {
    const success = await testEndpoint(endpoint, data);
    results.push({ endpoint, success });
    
    // Esperar un poco entre pruebas para no saturar el servidor
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Resumen final
  console.log('\n📊 RESUMEN DE PRUEBAS:');
  console.log('═'.repeat(50));
  
  let successful = 0;
  results.forEach(({ endpoint, success }) => {
    const status = success ? '✅ EXITOSO' : '❌ FALLIDO';
    console.log(`${status}  ${endpoint}`);
    if (success) successful++;
  });
  
  console.log('═'.repeat(50));
  console.log(`Total: ${successful}/${results.length} formularios funcionando correctamente`);
  
  if (successful === results.length) {
    console.log('\n🎉 ¡TODOS LOS FORMULARIOS ESTÁN FUNCIONANDO!');
    console.log('📧 Revisa la bandeja de entrada de diversiaeternals@gmail.com');
    console.log('✨ Sistema de emails automáticos completamente configurado');
  } else {
    console.log('\n⚠️  Algunos formularios necesitan atención');
  }
}

// Ejecutar pruebas
testAllForms().catch(console.error);