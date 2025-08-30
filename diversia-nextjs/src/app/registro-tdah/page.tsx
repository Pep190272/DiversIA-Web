'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';

const registroTDAHSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  apellidos: z.string().min(1, 'Los apellidos son requeridos'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  fecha_nacimiento: z.string().min(1, 'La fecha de nacimiento es requerida'),
  diagnostico_formal: z.boolean().optional(),
  habilidades: z.string().optional(),
  experiencia_laboral: z.string().optional(),
  formacion_academica: z.string().optional(),
  intereses_laborales: z.string().optional(),
  adaptaciones_necesarias: z.string().optional(),
  motivaciones: z.string().optional(),
  tipo_tdah: z.string().optional(),
  nivel_atencion: z.string().optional(),
  impulsividad: z.string().optional(),
  hiperactividad: z.string().optional(),
  medicacion: z.string().optional(),
});

type RegistroTDAHFormData = z.infer<typeof registroTDAHSchema>;

export default function RegistroTDAHPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<RegistroTDAHFormData>({
    resolver: zodResolver(registroTDAHSchema)
  });

  const onSubmit = async (data: RegistroTDAHFormData) => {
    setIsSubmitting(true);
    setMessage(null);

    try {
      const response = await fetch('/api/registro-tdah', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...data,
          diagnostico_formal: data.diagnostico_formal || false
        }),
      });

      const result = await response.json();

      if (result.success) {
        setMessage({ type: 'success', text: result.message });
        reset();
      } else {
        setMessage({ type: 'error', text: result.error || 'Error al procesar el registro' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error de conexión. Intenta de nuevo.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-100 py-12">
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
            Registro Especializado TDAH
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Formulario específicamente diseñado para personas con TDAH. Nos ayudará a entender 
            tus fortalezas únicas y crear un perfil laboral que destaque tu potencial.
          </p>
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 inline-block">
            <p className="text-orange-800">
              🧠 <strong>Especializado:</strong> Formulario adaptado para TDAH<br/>
              ⚡ <strong>Fortalezas:</strong> Destacamos tu creatividad y energía<br/>
              🎯 <strong>Personalizado:</strong> Matching con empresas inclusivas
            </p>
          </div>
        </div>

        {/* Formulario */}
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center text-orange-600 mb-8">
            Perfil Profesional TDAH
          </h2>
          
          {message && (
            <div className={`mb-6 p-4 rounded ${
              message.type === 'success' ? 'alert-success' : 'alert-error'
            }`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Información Personal */}
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="form-label">Nombre *</label>
                <input
                  {...register('nombre')}
                  type="text"
                  className="form-input"
                  placeholder="Tu nombre"
                />
                {errors.nombre && <p className="text-red-500 text-sm mt-1">{errors.nombre.message}</p>}
              </div>
              
              <div>
                <label className="form-label">Apellidos *</label>
                <input
                  {...register('apellidos')}
                  type="text"
                  className="form-input"
                  placeholder="Tus apellidos"
                />
                {errors.apellidos && <p className="text-red-500 text-sm mt-1">{errors.apellidos.message}</p>}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="form-label">Email *</label>
                <input
                  {...register('email')}
                  type="email"
                  className="form-input"
                  placeholder="tu@email.com"
                />
                {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
              </div>
              
              <div>
                <label className="form-label">Teléfono</label>
                <input
                  {...register('telefono')}
                  type="tel"
                  className="form-input"
                  placeholder="+34 600 000 000"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="form-label">Ciudad *</label>
                <input
                  {...register('ciudad')}
                  type="text"
                  className="form-input"
                  placeholder="Tu ciudad"
                />
                {errors.ciudad && <p className="text-red-500 text-sm mt-1">{errors.ciudad.message}</p>}
              </div>
              
              <div>
                <label className="form-label">Fecha de Nacimiento *</label>
                <input
                  {...register('fecha_nacimiento')}
                  type="date"
                  className="form-input"
                />
                {errors.fecha_nacimiento && <p className="text-red-500 text-sm mt-1">{errors.fecha_nacimiento.message}</p>}
              </div>
            </div>

            {/* Información TDAH Específica */}
            <div className="border-t pt-6">
              <h3 className="text-xl font-semibold mb-4 text-orange-600">Información TDAH</h3>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Tipo de TDAH</label>
                  <select {...register('tipo_tdah')} className="form-input">
                    <option value="">Selecciona una opción</option>
                    <option value="Inatento">Predominantemente Inatento</option>
                    <option value="Hiperactivo-Impulsivo">Hiperactivo-Impulsivo</option>
                    <option value="Combinado">Combinado</option>
                    <option value="No especificado">No especificado</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">Nivel de Atención</label>
                  <select {...register('nivel_atencion')} className="form-input">
                    <option value="">Selecciona</option>
                    <option value="Alto">Alto (me concentro bien)</option>
                    <option value="Medio">Medio (variable según el contexto)</option>
                    <option value="Bajo">Bajo (me cuesta concentrarme)</option>
                  </select>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4 mt-4">
                <div>
                  <label className="form-label">Nivel de Impulsividad</label>
                  <select {...register('impulsividad')} className="form-input">
                    <option value="">Selecciona</option>
                    <option value="Alto">Alto</option>
                    <option value="Medio">Medio</option>
                    <option value="Bajo">Bajo</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">Nivel de Hiperactividad</label>
                  <select {...register('hiperactividad')} className="form-input">
                    <option value="">Selecciona</option>
                    <option value="Alto">Alto</option>
                    <option value="Medio">Medio</option>
                    <option value="Bajo">Bajo</option>
                  </select>
                </div>
              </div>

              <div className="mt-4">
                <label className="form-label">Medicación</label>
                <select {...register('medicacion')} className="form-input">
                  <option value="">Selecciona</option>
                  <option value="Si, tomo medicación">Sí, tomo medicación</option>
                  <option value="No tomo medicación">No tomo medicación</option>
                  <option value="A veces">A veces / Según necesidad</option>
                  <option value="Prefiero no decir">Prefiero no decir</option>
                </select>
              </div>

              <div className="mt-4">
                <label className="flex items-center">
                  <input
                    {...register('diagnostico_formal')}
                    type="checkbox"
                    className="mr-2"
                  />
                  <span className="text-sm">Tengo diagnóstico formal de TDAH</span>
                </label>
              </div>
            </div>

            {/* Información Laboral */}
            <div className="border-t pt-6">
              <h3 className="text-xl font-semibold mb-4">Información Laboral</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="form-label">Habilidades y Fortalezas</label>
                  <textarea
                    {...register('habilidades')}
                    className="form-input"
                    rows={3}
                    placeholder="Ej: Creatividad, multitarea, pensamiento fuera de la caja, energía..."
                  />
                </div>

                <div>
                  <label className="form-label">Experiencia Laboral</label>
                  <textarea
                    {...register('experiencia_laboral')}
                    className="form-input"
                    rows={3}
                    placeholder="Resume tu experiencia laboral..."
                  />
                </div>

                <div>
                  <label className="form-label">Formación Académica</label>
                  <textarea
                    {...register('formacion_academica')}
                    className="form-input"
                    rows={2}
                    placeholder="Estudios, certificaciones, cursos..."
                  />
                </div>

                <div>
                  <label className="form-label">Intereses Laborales</label>
                  <textarea
                    {...register('intereses_laborales')}
                    className="form-input"
                    rows={2}
                    placeholder="¿En qué áreas te gustaría trabajar?"
                  />
                </div>

                <div>
                  <label className="form-label">Adaptaciones Necesarias</label>
                  <textarea
                    {...register('adaptaciones_necesarias')}
                    className="form-input"
                    rows={2}
                    placeholder="Ej: Espacios sin ruido, pausas frecuentes, tareas variadas..."
                  />
                </div>

                <div>
                  <label className="form-label">Motivaciones</label>
                  <textarea
                    {...register('motivaciones')}
                    className="form-input"
                    rows={2}
                    placeholder="¿Qué te motiva profesionalmente?"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full btn-primary text-lg py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Guardando perfil...' : 'Crear Perfil TDAH'}
            </button>
          </form>
        </div>

        {/* Info adicional */}
        <div className="max-w-2xl mx-auto mt-12 text-center">
          <h3 className="text-xl font-semibold mb-4">¿Sabías que las personas con TDAH...?</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-2xl mb-2">⚡</div>
              <h4 className="font-medium mb-2">Son Muy Creativas</h4>
              <p className="text-sm text-gray-600">
                Suelen generar ideas innovadoras y soluciones únicas
              </p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <div className="text-2xl mb-2">🎯</div>
              <h4 className="font-medium mb-2">Hiperfoco</h4>
              <p className="text-sm text-gray-600">
                Pueden concentrarse intensamente en tareas que les interesan
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}