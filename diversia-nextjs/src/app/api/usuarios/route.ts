import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    // Obtener todos los usuarios (similar a la API Flask)
    const users = await prisma.user.findMany({
      orderBy: {
        created_at: 'desc'
      }
    });

    const generalLeads = await prisma.generalLead.findMany({
      orderBy: {
        created_at: 'desc'
      }
    });

    const neurodivergentProfiles = await prisma.neurodivergentProfile.findMany({
      orderBy: {
        created_at: 'desc'
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        users,
        general_leads: generalLeads,
        neurodivergent_profiles: neurodivergentProfiles,
        total_users: users.length,
        total_general_leads: generalLeads.length,
        total_neurodivergent_profiles: neurodivergentProfiles.length
      }
    });
  } catch (error) {
    console.error('Error fetching users:', error);
    return NextResponse.json(
      { success: false, error: 'Error al obtener usuarios' },
      { status: 500 }
    );
  }
}