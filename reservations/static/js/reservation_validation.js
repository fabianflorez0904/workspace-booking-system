document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('reservation-form');
    const errorMessage = document.getElementById('error-message');
    const maxDays = 14;
    
    // Configurar fechas permitidas
    const dateInput = document.getElementById('date');
    const today = new Date();
    today.setHours(0,0,0,0);
    const maxDate = new Date(today);
    maxDate.setDate(today.getDate() + maxDays);
    
    dateInput.min = today.toISOString().split('T')[0];
    dateInput.max = maxDate.toISOString().split('T')[0];
    
    // Configurar límites de tiempo en los selectores
    const startTimeInput = document.getElementById('start_time');
    const endTimeInput = document.getElementById('end_time');
    startTimeInput.min = '07:00';
    startTimeInput.max = '22:59'; // Permite inicio hasta las 22:59 para no exceder 23:00 al sumar 8 hrs
    endTimeInput.min = '07:00';
    endTimeInput.max = '23:00';   // Fin máximo 23:00

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        errorMessage.classList.add('d-none');
        errorMessage.innerHTML = '';

        // Obtener valores
        const people = parseInt(document.getElementById('people').value);
        const date = document.getElementById('date').value;
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;
        let errors = [];

        // Validar que los campos no estén vacíos y sean correctos
        if (!people || people <= 0) {
            errors.push('Debe ingresar un número válido de personas.');
        }
        if (!date) {
            errors.push('Debe seleccionar una fecha.');
        }
        if (!startTime || !endTime) {
            errors.push('Debe seleccionar un horario de inicio y fin.');
        }
        
        // Convertir la fecha seleccionada en objeto Date

        const selectedDate = new Date(date + 'T00:00:00');
        if (selectedDate < today || selectedDate > maxDate) {
            errors.push('La fecha debe estar dentro de los próximos 14 días.');
        }

        // Validar horarios: convertir tiempos a objetos Date usando una fecha ficticia
        const start = new Date(`2000-01-01T${startTime}`);
        const end = new Date(`2000-01-01T${endTime}`);
        const minAllowed = new Date('2000-01-01T07:00');
        const maxAllowed = new Date('2000-01-01T23:00');

        if (start < minAllowed) {
            errors.push('La hora de inicio no puede ser antes de las 07:00 AM.');
        }
        if (end > maxAllowed) {
            errors.push('La hora de fin no puede ser posterior a las 11:00 PM.');
        }
        if (start >= end) {
            errors.push('La hora de inicio debe ser anterior a la de fin.');
        }

        // Validar duración máxima (8 horas)
        const duration = (end - start) / (1000 * 60 * 60); // duración en horas
        if (duration > 8) {
            errors.push('La duración máxima permitida es de 8 horas.');
        }
        
        // Si la fecha es hoy, validar que la hora de inicio sea posterior a la hora actual
        if (selectedDate.getTime() === today.getTime()) {
            const now = new Date();
            const [startH, startM] = startTime.split(':');
            const startToday = new Date();
            startToday.setHours(parseInt(startH), parseInt(startM), 0, 0);
            if (startToday <= now) {
                errors.push('Para hoy, la hora de inicio debe ser posterior a la hora actual.');
            }
        }

        // Mostrar errores o enviar formulario
        if (errors.length > 0) {
            errorMessage.innerHTML = `
                <h5 class="alert-heading">¡Error en la reservación!</h5>
                <ul class="mb-0">
                    ${errors.map(e => `<li>${e}</li>`).join('')}
                </ul>
            `;
            errorMessage.classList.remove('d-none');
        } else {
            form.submit();
        }
    });
});
