window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        geojson_filter: function(feature, context) {return context.hideout.ugas_selected.includes(feature.properties.uga) && context.hideout.spes_selected.includes(feature.properties.spe) && context.hideout.cib_selected.includes(feature.properties.cib) && context.hideout.pvm_range[0]<feature.properties.pvm && context.hideout.pvm_range[1]>feature.properties.pvm;},
        pharmas_filter: function(feature, context) {return context.hideout.ugas_selected.includes(feature.properties.uga) && context.hideout.cib_selected.includes(feature.properties.cib_vm);},
        uga_geojson_filter: function(feature, context) {return context.hideout.selected.includes(feature.properties.CODE_UGA);},
        cible_icon: function(feature, latlng) {
            const doctor_colors = {
                'GY': '#bd0071',
                'MGY': '#bd0071',
                'SF': '#bd0071',
                'MG': '#ffff46',
                'GE': '#fe7600',
                'PE': '#0080ff',
                'PPSY': '#410E66',
                'PSY': '#410E66',
                'NE': '#410e66',
                '': '#000000'
            };
            if (feature.properties.cib > 0) {
                var shape = 'star'
            } else {
                var shape = 'square'
            };
            const marker = L.ExtraMarkers.icon({
                icon: 'fa-user-doctor',
                prefix: 'fa',
                markerColor: doctor_colors[feature.properties.spe],
                iconColor: 'white',
                shape: shape,
                svg: true
            })
            var m = L.marker(latlng, {
                icon: marker
            });
            var tooltip = L.tooltip(latlng, {direction: 'top', content: feature.properties.nom, offset: L.point(0, -40)});
            m.bindTooltip(tooltip)
            return m
        },
        pharmas_icon: function(feature, latlng) {
            if (feature.properties.cib_vm > 0) {
                var shape = 'star'
            } else {
                var shape = 'square'
            };
            const pmarker = L.ExtraMarkers.icon({
                icon: 'fa-prescription-bottle-medical',
                prefix: 'fa',
                markerColor: 'green',
                iconColor: 'white',
                shape: shape,
            });
            var m = L.marker(latlng, {
                icon: pmarker
            });
            var tooltip = L.tooltip(latlng, {direction: 'top', content: feature.properties.nom, offset: L.point(0, -40)});
            m.bindTooltip(tooltip)
            return m
        },
        uga_style_handle: function(feature, context){
            const uga_colors = {
                '75AUT': '#164863',
                '75PAS': '#427D9D',
                '75TRO': '#9BBEC8',
                '75INV': '#1b7a02',
                '75ELY': '#A7D129',
                '75GRE': '#9A1663',
                '75VAU': '#E0144C',
                '75MNP': '#FF5858',
                '75PER': '#ec863d',
                '75TER': '#FE7600',
                '92LEV': '#994D1C',
                '92NEU': '#E48F45'
            };
            return {fillColor: uga_colors[feature.properties.CODE_UGA], fillOpacity: 0.3,  color: uga_colors[feature.properties.CODE_UGA], opacity: 1, weight:5, dashArray: '5'}
        },
        flipCard: function() {
            var card = getCard(this)
            card.classList.toggle('flip')
        },
        getBodyCard: function(shield) {
            return shield.parentElement.parentElement.childNodes[5].childNodes[1];
        },
        getBackBodyCard: function(shield) {
            return shield.parentElement.parentElement.nextElementSibling.childNodes[5];
        },
        toggleBodyCard: function() {
            var bodycard = getBodyCard(this)
            bodycard.classList.toggle('hide')
            var bbodycard = getBackBodyCard(this)
            bbodycard.classList.toggle('hide')
            var complete = this.parentElement.parentElement.parentElement.parentElement.parentElement
            complete.classList.toggle('small')
        },
        toggleAllBodyCards: function() {
            const bodycards = toArray(document.getElementsByClassName('card-body'))
            bodycards.forEach( (bodycard) => bodycard.classList.toggle('hide'))
            const cards = toArray(document.getElementsByClassName('complete-card'))
            cards.forEach( (card) => card.classList.toggle('small'))
        },
        changeTooltip: function() {
            const tooltipsRight = toArray(document.getElementsByClassName('leaflet-tooltip-right'))
            if (tooltipsRight.length > 0) {
                tooltipsRight[0].classList = "leaflet-tooltip-pane leaflet-tooltip-top"
            }
            const tooltipsLeft = toArray(document.getElementsByClassName('leaflet-tooltip-left'))
            if (tooltipsLeft.length > 0) {
                tooltipsLeft[0].classList = "leaflet-tooltip-pane leaflet-tooltip-top"
            }
        }
    }
});