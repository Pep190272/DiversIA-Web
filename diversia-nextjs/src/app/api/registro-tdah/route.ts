import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';

const registroTDAHSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  apellidos: z.string().min(1, 'Los apellidos son requeridos'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  fecha_nacimiento: z.string(),
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

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = registroTDAHSchema.parse(body);

    // Verificar si ya existe un perfil con este email
    const existingProfile = await prisma.neurodivergentProfile.findFirst({
      where: { email: validatedData.email }
    });

    if (existingProfile) {
      // Actualizar el perfil existente
      const updatedProfile = await prisma.neurodivergentProfile.update({
        where: { id: existingProfile.id },
        data: {
          nombre: validatedData.nombre,
          apellidos: validatedData.apellidos,
          telefono: validatedData.telefono,
          ciudad: validatedData.ciudad,
          fecha_nacimiento: new Date(validatedData.fecha_nacimiento),
          tipo_neurodivergencia: 'TDAH',
          diagnostico_formal: validatedData.diagnostico_formal || false,
          habilidades: validatedData.habilidades,
          experiencia_laboral: validatedData.experiencia_laboral,
          formacion_academica: validatedData.formacion_academica,
          intereses_laborales: validatedData.intereses_laborales,
          adaptaciones_necesarias: validatedData.adaptaciones_necesarias,
          motivaciones: validatedData.motivaciones,
          tipo_tdah: validatedData.tipo_tdah,
          nivel_atencion: validatedData.nivel_atencion,
          impulsividad: validatedData.impulsividad,
          hiperactividad: validatedData.hiperactividad,
          medicacion: validatedData.medicacion,
          updated_at: new Date(),
        }
      });

      return NextResponse.json({
        success: true,
        message: `¡Perfil TDAH actualizado exitosamente, ${validatedData.nombre}!`,
        data: updatedProfile
      });
    }

    // Crear nuevo perfil TDAH
    const newProfile = await prisma.neurodivergentProfile.create({
      data: {
        nombre: validatedData.nombre,
        apellidos: validatedData.apellidos,
        email: validatedData.email,
        telefono: validatedData.telefono,
        ciudad: validatedData.ciudad,
        fecha_nacimiento: new Date(validatedData.fecha_nacimiento),
        tipo_neurodivergencia: 'TDAH',
        diagnostico_formal: validatedData.diagnostico_formal || false,
        habilidades: validatedData.habilidades,
        experiencia_laboral: validatedData.experiencia_laboral,
        formacion_academica: validatedData.formacion_academica,
        intereses_laborales: validatedData.intereses_laborales,
        adaptaciones_necesarias: validatedData.adaptaciones_necesarias,
        motivaciones: validatedData.motivaciones,
        tipo_tdah: validatedData.tipo_tdah,
        nivel_atencion: validatedData.nivel_atencion,
        impulsividad: validatedData.impulsividad,
        hiperactividad: validatedData.hiperactividad,
        medicacion: validatedData.medicacion,
      }
    });

    return NextResponse.json({
      success: true,
      message: `¡Registro TDAH completado exitosamente, ${validatedData.nombre}! Tu perfil detallado ha sido guardado.`,
      data: newProfile
    });

  } catch (error) {
    console.error('Error processing TDAH registration:', error);
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { success: false, error: 'Datos de formulario inválidos', details: error.errors },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { success: false, error: 'Error al procesar el registro TDAH' },
      { status: 500 }
    );
  }
}