import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';

const registroSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  apellidos: z.string().min(1, 'Los apellidos son requeridos'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  fecha_nacimiento: z.string(),
  tipo_neurodivergencia: z.string().optional(),
  diagnostico_formal: z.boolean().optional(),
  habilidades: z.string().optional(),
  experiencia_laboral: z.string().optional(),
  formacion_academica: z.string().optional(),
  intereses_laborales: z.string().optional(),
  adaptaciones_necesarias: z.string().optional(),
  motivaciones: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = registroSchema.parse(body);

    // Verificar si el email ya existe
    const existingLead = await prisma.generalLead.findUnique({
      where: { email: validatedData.email }
    });

    if (existingLead) {
      // Actualizar el lead existente
      const updatedLead = await prisma.generalLead.update({
        where: { email: validatedData.email },
        data: {
          nombre: validatedData.nombre,
          apellidos: validatedData.apellidos,
          telefono: validatedData.telefono,
          ciudad: validatedData.ciudad,
          fecha_nacimiento: new Date(validatedData.fecha_nacimiento),
          tipo_neurodivergencia: validatedData.tipo_neurodivergencia,
          diagnostico_formal: validatedData.diagnostico_formal || false,
          habilidades: validatedData.habilidades,
          experiencia_laboral: validatedData.experiencia_laboral,
          formacion_academica: validatedData.formacion_academica,
          intereses_laborales: validatedData.intereses_laborales,
          adaptaciones_necesarias: validatedData.adaptaciones_necesarias,
          motivaciones: validatedData.motivaciones,
          updated_at: new Date(),
        }
      });

      return NextResponse.json({
        success: true,
        message: `¡Test actualizado exitosamente, ${validatedData.nombre}! Tu información ha sido actualizada.`,
        data: updatedLead
      });
    }

    // Crear nuevo lead
    const newLead = await prisma.generalLead.create({
      data: {
        nombre: validatedData.nombre,
        apellidos: validatedData.apellidos,
        email: validatedData.email,
        telefono: validatedData.telefono,
        ciudad: validatedData.ciudad,
        fecha_nacimiento: new Date(validatedData.fecha_nacimiento),
        tipo_neurodivergencia: validatedData.tipo_neurodivergencia,
        diagnostico_formal: validatedData.diagnostico_formal || false,
        habilidades: validatedData.habilidades,
        experiencia_laboral: validatedData.experiencia_laboral,
        formacion_academica: validatedData.formacion_academica,
        intereses_laborales: validatedData.intereses_laborales,
        adaptaciones_necesarias: validatedData.adaptaciones_necesarias,
        motivaciones: validatedData.motivaciones,
      }
    });

    return NextResponse.json({
      success: true,
      message: `¡Test completado exitosamente, ${validatedData.nombre}! Tu información ha sido guardada. Te contactaremos pronto con información sobre formularios específicos.`,
      data: newLead
    });

  } catch (error) {
    console.error('Error processing registration:', error);
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { success: false, error: 'Datos de formulario inválidos', details: error.errors },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { success: false, error: 'Error al procesar el registro' },
      { status: 500 }
    );
  }
}