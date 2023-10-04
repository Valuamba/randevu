from randevu.test.factory import register


@register
def appointment(self, employee, **kwargs):
    category = self.mixer.blend('service.Category')
    service = self.mixer.blend('service.SalonService')
    if 'client' not in kwargs.keys():
        kwargs['client'] = self.mixer.blend('client.Client', phone='+48731331105')

    appointment = self.mixer.blend('appointment.Appointment', category=category, service=service,
        day = '2022-12-25',
        employee = employee,
        time_step = 35,
        **kwargs
    )

    return appointment
