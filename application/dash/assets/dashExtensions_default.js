window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        geojson_filter: function(feature, context) {return context.hideout.ugas_selected.includes(feature.properties.uga) && context.hideout.spes_selected.includes(feature.properties.spe) && context.hideout.cib_selected.includes(feature.properties.cib) && context.hideout.pvm_range[0]<feature.properties.pvm && context.hideout.pvm_range[1]>feature.properties.pvm;},
        uga_geojson_filter: function(feature, context) {return context.hideout.selected.includes(feature.properties.CODE_UGA);},
        cible_icon: function(feature, latlng) {
            const doctor_colors = {
                'GY': '#bd0071',
                'MGY': '#bd0071',
                'SF': '#bd0071',
                'MG': '#aaa',
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
            if (feature.properties.spe !== '') {
                const marker = L.ExtraMarkers.icon({
                    icon: 'fa-user-doctor',
                    prefix: 'fa',
                    markerColor: doctor_colors[feature.properties.spe],
                    iconColor: 'white',
                    shape: shape,
                    svg: true
                });
                return L.marker(latlng, {
                    icon: marker
                });
            } else {
                const pmarker = L.ExtraMarkers.icon({
                    icon: 'fa-prescription-bottle-medical',
                    prefix: 'fa',
                    markerColor: 'green',
                    iconColor: 'white',
                    shape: 'circle',
                });
                return L.marker(latlng, {
                    icon: pmarker
                });
            }
        },
        uga_style_handle: function(feature, context){
            const uga_colors = {
                '75AUT': '#ff0000',
                '75PAS': '#bd0071',
                '75TRO': '#410E66',
                '75INV': '#130066',
                '75ELY': '#fe7600',
                '75GRE': '#060087',
                '75VAU': '#00877d',
                '75MNP': '#008000',
                '75PER': '#32cd32',
                '75TER': '#00ffe1',
                '92LEV': '#adff2f',
                '92NEU': '#f3ff00'
            };
            return {fillColor: uga_colors[feature.properties.CODE_UGA], fillOpacity: 0.3,  color: uga_colors[feature.properties.CODE_UGA], opacity: 1, weight:5, dashArray: '5'}
        },
        search: function () {
            $.fn.DataTable.ext.search.push((_,__,i) => {

                const dataTable = $('datatable').DataTable({dom:'t',data:srcData,columns:[{title:'Id',data:'id'},{title:'Item',data:'item',render:data=>`<input value="${data}"></input>`},{title:'Category',data:'category',render:data=>`<select>${['fruit', 'vegie', 'berry'].reduce((options, item) => options+='<option value="'+item+'" '+(item == data ? 'selected' : '')+'>'+item+'</option>', '<option value=""></option>')}</select>`}]});
                const currentTr = dataTable.row(i).node();
              const inputMatch = $(currentTr)
                .find('select,input')
                .toArray()
                .some(input => $(input).val().toLowerCase().includes( $('#search').val().toLowerCase()));
              const textMatch = $(currentTr)
                .children()
                .not('td:has("input,select")')
                .toArray()
                .some(td => $(td).text().toLowerCase().includes($('#search').val().toLowerCase()))
              return inputMatch || textMatch || $('#search').val() == ''
            });

            $('#search').on('keyup', () => dataTable.draw());
        }
    }
});