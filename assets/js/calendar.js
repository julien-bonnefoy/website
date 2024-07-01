window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_calendar: function(n, data) {
            const colors = {
                'GY': {'bgc': 'bg-gradient-faded-danger-vertical', 'tc': '#fff'},
                'MGY': {'bgc': 'bg-gradient-faded-danger-vertical', 'tc': '#fff'},
                'SF': {'bgc': 'bg-gradient-faded-danger-vertical', 'tc': '#fff'},
                'MG': {'bgc': 'bg-gradient-faded-secondary', 'tc': '#000'},
                'GE': {'bgc': 'bg-gradient-warning', 'tc': '#fff'},
                'PE': {'bgc': 'bg-gradient-info', 'tc': '#fff'},
                'PPSY': {'bgc': 'bg-gradient-primary', 'tc': '#fff'},
                'PSY': {'bgc': 'bg-gradient-primary', 'tc': '#fff'},
                'NE': {'bgc': 'bg-gradient-primary', 'tc': '#fff'},
                '': {'bgc': '#000000', 'tc': '#fff'}
            };
            // console.log(colors);
            var rdv = data.filter(function(d) {
                return d.ddv > 0;
            });
            var events = [];
            function pad(num, size) {
                var s = "000000000" + num;
                return s.substr(s.length-size);
            };
            for (var i = 0; i < rdv.length; i++) {
                var r = rdv[i];
                var bordercolor = 'transparent'
                if (r.c24c1 > 0) {
                    bordercolor = 'red'
                }
                // console.log(pad(r.id,4), r.nom, r.pre, r.spe1, new Date(r.ddv*1000).toLocaleString());
                events.push({
                    id: pad(r.id,4),
                    title: r.pre + ' ' + r.nom,
                    start: new Date(r.ddv*1000),
                    classNames: new Array(colors[r.spe1].bgc, pad(r.id, 4)),
                    textColor: colors[r.spe1].tc,
                    borderColor: bordercolor,
                    extendedProps: {
                        spe: r.spe1
                    }
                })
            };

            var calendar = new FullCalendar.Calendar( document.getElementById('calendar'), {
              timeZone: 'UTC',
              contentHeight: 'auto',
              editable: true,
              selectable: true,
              aspectRatio: 2,
              initialView: 'dayGridMonth',
              views: {
                month: {
                  titleFormat: {
                    month: "long",
                    year: "numeric"
                  }
                },
                agendaWeek: {
                  titleFormat: {
                    month: "long",
                    year: "numeric",
                    day: "numeric"
                  }
                },
                agendaDay: {
                  titleFormat: {
                    month: "short",
                    year: "numeric",
                    day: "numeric"
                  }
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
              },
              eventTimeFormat: { // like '14:30:00'
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
              },
              eventClick: function (info) {
                alert('Clicked on: ' + info.event.title);
              },
              dateClick: function(date, jsEvent, view) {
                alert('Clicked on: ' + date.format());
              }
            });
            return calendar.render();
        }
    }
});
