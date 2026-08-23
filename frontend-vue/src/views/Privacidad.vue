<script setup lang="ts">
const email = import.meta.env.VITE_CONTACT_EMAIL || '';
const numero = import.meta.env.VITE_WHATSAPP_NUMBER || '56944830378';
</script>

<template>
  <section class="py-5">
    <div class="container" style="max-width: 820px">
      <h1 class="display-6 fw-bold mb-4">Política de Privacidad</h1>
      <p class="text-secondary small">Última actualización: agosto de 2026</p>

      <div class="text-secondary">
        <h2 class="h5 text-orion-primary mt-4">1. Quién trata sus datos</h2>
        <p>
          El responsable del tratamiento es Orion, productora de eventos con operación en Chile.
          Puede contactarnos por WhatsApp al +{{ numero }}<span v-if="email"> o al correo
          <a class="link-light" :href="`mailto:${email}`">{{ email }}</a></span>.
        </p>

        <h2 class="h5 text-orion-primary mt-4">2. Qué datos recopilamos</h2>
        <p>
          Solo los que usted nos entrega voluntariamente en el formulario de cotización: nombre,
          correo electrónico, teléfono (opcional), empresa (opcional), tipo de evento, descripción
          del evento, fecha estimada y presupuesto estimado (opcional). No recopilamos datos
          sensibles ni datos de menores de edad.
        </p>

        <h2 class="h5 text-orion-primary mt-4">3. Para qué los usamos</h2>
        <p>
          Exclusivamente para responder su solicitud, elaborar la cotización y, si contrata,
          coordinar la producción del evento. No los usamos para publicidad de terceros ni los
          vendemos.
        </p>

        <h2 class="h5 text-orion-primary mt-4">4. Base legal</h2>
        <p>
          El tratamiento se funda en su consentimiento al enviar el formulario y en las medidas
          precontractuales necesarias para atender su solicitud, conforme a la Ley N.º 19.628 sobre
          Protección de la Vida Privada y la Ley N.º 21.719 que la moderniza.
        </p>

        <h2 class="h5 text-orion-primary mt-4">5. Con quién los compartimos</h2>
        <p>
          Con nadie con fines comerciales. Los datos se almacenan en nuestra propia base de datos y
          se envía una notificación interna por correo electrónico al equipo de Orion cuando llega
          una nueva solicitud. Solo podrían compartirse con proveedores estrictamente necesarios
          para ejecutar el evento contratado, o cuando la ley lo exija.
        </p>

        <h2 class="h5 text-orion-primary mt-4">6. Cuánto tiempo los conservamos</h2>
        <p>
          Mantenemos las solicitudes de cotización mientras exista una relación comercial vigente o
          un interés legítimo en retomarla, y las eliminamos cuando usted lo solicita o cuando
          dejan de ser necesarias.
        </p>

        <h2 class="h5 text-orion-primary mt-4">7. Sus derechos</h2>
        <p>
          Usted puede acceder a sus datos, rectificarlos, cancelarlos, oponerse a su tratamiento y
          solicitar su portabilidad (derechos ARCO+). Para ejercerlos escríbanos por los canales
          indicados en el punto 1; responderemos dentro de los plazos legales.
        </p>

        <h2 class="h5 text-orion-primary mt-4">8. Cookies y analítica</h2>
        <p>
          Este sitio no usa cookies publicitarias ni de perfilamiento. Utilizamos almacenamiento
          local del navegador únicamente para recordar su preferencia de tema (claro u oscuro). Si
          en el futuro incorporamos herramientas de analítica, se le pedirá su consentimiento antes
          de activarlas y podrá rechazarlas sin perder funcionalidad.
        </p>

        <h2 class="h5 text-orion-primary mt-4">9. Seguridad</h2>
        <p>
          Aplicamos medidas razonables de seguridad técnica y organizativa para proteger sus datos
          frente a accesos no autorizados, pérdida o alteración. El acceso al panel de
          administración está restringido y autenticado.
        </p>

        <h2 class="h5 text-orion-primary mt-4">10. Cambios en esta política</h2>
        <p>
          Podemos actualizar esta política. La versión vigente siempre será la publicada en esta
          página, con su fecha de última actualización.
        </p>
      </div>
    </div>
  </section>
</template>
