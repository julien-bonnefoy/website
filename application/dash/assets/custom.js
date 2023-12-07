window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
		render_calendar: function(n, data) {
            const doctor_colors = {
                'GY': {'bgc': '#bd0071', 'tc': '#fff'},
                'MGY': {'bgc': '#bd0071', 'tc': '#fff'},
                'SF': {'bgc': '#bd0071', 'tc': '#fff'},
                'MG': {'bgc': '#ffff46', 'tc': '#000'},
                'GE': {'bgc': '#fe7600', 'tc': '#fff'},
                'PE': {'bgc': '#0080ff', 'tc': '#fff'},
                'PPSY': {'bgc': '#410E66', 'tc': '#fff'},
                'PSY': {'bgc': '#410E66', 'tc': '#fff'},
                'NE': {'bgc': '#410e66', 'tc': '#fff'},
                '': {'bgc': '#000000', 'tc': '#fff'}
            };
            var rdv = data.filter(function(d) {
                return d.ddv > 0;
            });
            var events = []
            for (let i = 0; i < rdv.length; i++) {
                var r = rdv[i]
                events.push({
                    title: r.nom,
                    start: new Date(r.ddv*1000),
                    backgroundColor: doctor_colors[r.spe]['bgc'],
                    textColor: doctor_colors[r.spe]['tc'],
                });
            }
            console.log(events);
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
              timeZone: 'UTC',
              editable: true,
              selectable: true,
              aspectRatio: 3,
              initialView: 'dayGridFourWeek',
              views: {
                dayGridFourWeek: {
                  type: 'dayGrid',
                  duration: { weeks: 4 },
                  buttonText: 'month'
                }
              },
              locale: 'fr',
              nowIndicator: true,
              firstDay: 1,
              events: events,
              headerToolbar: {
                left: 'prev,next',
                center: 'title',
                right: 'today,dayGridYear,dayGridFourWeek,timeGridWeek,timeGridDay' // user can switch between the two
              }
            });
            return calendar.render();
        }
    }
});
