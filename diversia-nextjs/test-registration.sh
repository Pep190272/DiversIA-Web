#!/bin/bash

echo "🧪 Probando sistema de registro con emails..."

# Test del formulario general
echo "📝 Test 1: Formulario general de registro"
curl -X POST http://localhost:3000/api/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Usuario",
    "apellidos": "Email Prueba", 
    "email": "diversiaeternals@gmail.com",
    "telefono": "+34 600 000 000",
    "ciudad": "Madrid",
    "fecha_nacimiento": "1990-01-01",
    "tipo_neurodivergencia": "TDAH",
    "habilidades": "Prueba de habilidades",
    "experiencia_laboral": "Prueba de experiencia",
    "motivaciones": "Probar sistema de emails"
  }'

echo -e "\n\n📝 Test 2: Formulario específico TDAH"
curl -X POST http://localhost:3000/api/registro-tdah \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test TDAH",
    "apellidos": "Email Prueba",
    "email": "diversiaeternals@gmail.com", 
    "telefono": "+34 600 000 000",
    "ciudad": "Barcelona",
    "fecha_nacimiento": "1985-05-15",
    "tipo_tdah": "Combinado",
    "nivel_atencion": "Medio",
    "habilidades": "Creatividad y energía",
    "motivaciones": "Probar formulario TDAH con emails"
  }'

echo -e "\n\n✅ Tests completados. Revisa tu email diversiaeternals@gmail.com para verificar los emails."