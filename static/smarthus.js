const smarthus = (() => {

    const init = async () => {
        await displayLights()
        addListeners()
    }

    const displayLights = async () => {
        return $.get('/devices', (lights) => {
            const $lightsDiv = $('#lights')
            lights.forEach(light => {
                $lightsDiv.append(createButton(light))
            })
        })
    };

    const addListeners = () => {
        $('#night').on('click', turnOfAll)
        $('#morning').on('click', turnOnSome)
        $('#lights .button').on('click', toggle)
    }

    // needs to be a function to be able to access $(this)
    const toggle = function() {
        const id = $(this).attr('id').substring(5)
        $.post(`/devices/toggle/${id}`, updateColorOn)
    };

    const turnOfAll = () => {
        const $night = $("#night");
        $night.addClass('is-loading')
        setTimeout(async () => {
            await $.post('/devices/turnOffAll', updateLights)
            $night.removeClass('is-loading')
        }, 50)
    }

    const turnOnSome = () => {
        const $morning = $("#morning");
        $morning.addClass('is-loading')
        setTimeout(async () => {
            await $.post('/devices/turnOnSome', updateLights)
            $morning.removeClass('is-loading')
        }, 50)
    }

    const updateLights = (lights) => {
        lights.forEach(light => {
            updateColorOn(light, lights);
        })
    };

    const updateColorOn = (light) => {
        let $light = $(`#light${light.id}`);
        $light.removeClass('is-success')
            .removeClass('is-danger')
            .addClass('is-' + light.status)
            .text(light.label)
    };

    const createButton = light => `
        <div class="columns is-mobile">
            <div class="coulmn is-vertical-center">
                <p class="is-size-6 has-text-weight-medium">${light.name}</p>
            </div>
            <div class="column">
                <button id="light${light.id}" class="button is-${light.status} is-light is-pulled-right">${light.label}</button>
            </div>
        </div>
`;

    return {
        init: init,
    }
})();
