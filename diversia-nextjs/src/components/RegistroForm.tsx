'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const registroSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  apellidos: z.string().min(1, 'Los apellidos son requeridos'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  fecha_nacimiento: z.string().min(1, 'La fecha de nacimiento es requerida'),
  tipo_neurodivergencia: z.string().optional(),
  diagnostico_formal: z.boolean().optional(),
  habilidades: z.string().optional(),
  experiencia_laboral: z.string().optional(),
  formacion_academica: z.string().optional(),
  intereses_laborales: z.string().optional(),
  adaptaciones_necesarias: z.string().optional(),
  motivaciones: z.string().optional(),
});

type RegistroFormData = z.infer<typeof registroSchema>;

export default function RegistroForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<RegistroFormData>({
    resolver: zodResolver(registroSchema)
  });

  const onSubmit = async (data: RegistroFormData) => {
    setIsSubmitting(true);
    setMessage(null);

    try {
      const response = await fetch('/api/registro', {
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
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-3xl font-bold text-center text-blue-600 mb-8">
        Haz mi Test - DiversIA
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

        {/* Información de Neurodivergencia */}
        <div className="border-t pt-6">
          <h3 className="text-xl font-semibold mb-4">Información de Neurodivergencia</h3>
          
          <div>
            <label className="form-label">Tipo de Neurodivergencia</label>
            <select {...register('tipo_neurodivergencia')} className="form-input">
              <option value="">Selecciona una opción</option>
              <option value="TDAH">TDAH</option>
              <option value="TEA">TEA (Trastorno del Espectro Autista)</option>
              <option value="Dislexia">Dislexia</option>
              <option value="Discalculia">Discalculia</option>
              <option value="Disgrafía">Disgrafía</option>
              <option value="Altas Capacidades">Altas Capacidades</option>
              <option value="Otro">Otro</option>
              <option value="No tengo">No tengo neurodivergencia</option>
            </select>
          </div>

          <div className="mt-4">
            <label className="flex items-center">
              <input
                {...register('diagnostico_formal')}
                type="checkbox"
                className="mr-2"
              />
              <span className="text-sm">Tengo diagnóstico formal</span>
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
                placeholder="Describe tus principales habilidades..."
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
                placeholder="¿Qué adaptaciones necesitas en el trabajo?"
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
          {isSubmitting ? 'Enviando...' : 'Completar Test'}
        </button>
      </form>
    </div>
  );
}