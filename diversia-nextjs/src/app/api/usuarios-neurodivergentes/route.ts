import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    // Estadísticas para el CRM dashboard
    const [
      totalUsers,
      usersWithDiagnosis,
      generalLeads,
      neurodivergentProfiles,
      companies
    ] = await Promise.all([
      prisma.user.count(),
      prisma.user.count({
        where: {
          diagnostico_formal: true
        }
      }),
      prisma.generalLead.count(),
      prisma.neurodivergentProfile.count(),
      prisma.company.count()
    ]);

    // Obtener usuarios recientes
    const recentUsers = await prisma.user.findMany({
      take: 10,
      orderBy: {
        created_at: 'desc'
      },
      select: {
        id: true,
        nombre: true,
        apellidos: true,
        email: true,
        tipo_neurodivergencia: true,
        diagnostico_formal: true,
        created_at: true
      }
    });

    // Distribución por tipo de neurodivergencia
    const neurodivergenceDistribution = await prisma.user.groupBy({
      by: ['tipo_neurodivergencia'],
      _count: {
        tipo_neurodivergencia: true
      }
    });

    return NextResponse.json({
      success: true,
      stats: {
        total_users: totalUsers,
        users_with_diagnosis: usersWithDiagnosis,
        general_leads: generalLeads,
        neurodivergent_profiles: neurodivergentProfiles,
        companies: companies
      },
      recent_users: recentUsers,
      neurodivergence_distribution: neurodivergenceDistribution
    });
  } catch (error) {
    console.error('Error fetching neurodivergent users stats:', error);
    return NextResponse.json(
      { success: false, error: 'Error al obtener estadísticas' },
      { status: 500 }
    );
  }
}