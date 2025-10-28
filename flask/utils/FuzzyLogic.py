import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


def CalculateSprayingDelay(
    airTemperature: int | float, humidity: int | float, waterTemperature: int | float
) -> int:
    # Defining membership scope
    # Input
    airTemperatureMember = ctrl.Antecedent(
        np.arange(0, 35 + 1, 1), label="Air Temperature (°C)"
    )
    humidityMember = ctrl.Antecedent(np.arange(0, 100 + 1, 1), label="Humidity (%)")
    waterTemperatureMember = ctrl.Antecedent(
        np.arange(0, 35 + 1, 1), label="Water Temperature (°C)"
    )

    # Output
    delayMembership = ctrl.Consequent(np.arange(10, 50 + 1, 1), label="Delay (minutes)")

    # Create Membership Air Temperature
    airTemperatureMember["cold"] = fuzz.trapmf(
        airTemperatureMember.universe, [0, 0, 10, 15]
    )
    airTemperatureMember["optimal"] = fuzz.trapmf(
        airTemperatureMember.universe, [10, 15, 20, 25]
    )
    airTemperatureMember["hot"] = fuzz.trapmf(
        airTemperatureMember.universe, [20, 25, 35, 35]
    )

    # Create Membership Humidity
    humidityMember["dry"] = fuzz.trapmf(humidityMember.universe, [0, 0, 70, 75])
    humidityMember["optimal"] = fuzz.trapmf(humidityMember.universe, [70, 75, 85, 90])
    humidityMember["moist"] = fuzz.trapmf(humidityMember.universe, [85, 90, 100, 100])

    # Create Membership Water Temperature
    waterTemperatureMember["cold"] = fuzz.trapmf(
        waterTemperatureMember.universe, [0, 0, 13, 18]
    )
    waterTemperatureMember["optimal"] = fuzz.trapmf(
        waterTemperatureMember.universe, [13, 18, 22, 27]
    )
    waterTemperatureMember["hot"] = fuzz.trapmf(
        waterTemperatureMember.universe, [22, 27, 35, 35]
    )

    # Create Membership Spraying Delay
    delayMembership["short"] = fuzz.trapmf(delayMembership.universe, [10, 10, 20, 25])
    delayMembership["normal"] = fuzz.trapmf(delayMembership.universe, [20, 25, 35, 40])
    delayMembership["long"] = fuzz.trapmf(delayMembership.universe, [35, 40, 50, 50])

    rules = [
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["dry"]
            & waterTemperatureMember["cold"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["dry"]
            & waterTemperatureMember["optimal"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["dry"]
            & waterTemperatureMember["hot"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["optimal"]
            & waterTemperatureMember["cold"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["optimal"]
            & waterTemperatureMember["optimal"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["optimal"]
            & waterTemperatureMember["hot"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["moist"]
            & waterTemperatureMember["cold"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["moist"]
            & waterTemperatureMember["optimal"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["cold"]
            & humidityMember["moist"]
            & waterTemperatureMember["hot"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["dry"]
            & waterTemperatureMember["cold"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["dry"]
            & waterTemperatureMember["optimal"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["dry"]
            & waterTemperatureMember["hot"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["optimal"]
            & waterTemperatureMember["cold"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["optimal"]
            & waterTemperatureMember["optimal"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["optimal"]
            & waterTemperatureMember["hot"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["moist"]
            & waterTemperatureMember["cold"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["moist"]
            & waterTemperatureMember["optimal"],
            delayMembership["long"],
        ),
        ctrl.Rule(
            airTemperatureMember["optimal"]
            & humidityMember["moist"]
            & waterTemperatureMember["hot"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["dry"]
            & waterTemperatureMember["cold"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["dry"]
            & waterTemperatureMember["optimal"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["dry"]
            & waterTemperatureMember["hot"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["optimal"]
            & waterTemperatureMember["cold"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["optimal"]
            & waterTemperatureMember["optimal"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["optimal"]
            & waterTemperatureMember["hot"],
            delayMembership["short"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["moist"]
            & waterTemperatureMember["cold"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["moist"]
            & waterTemperatureMember["optimal"],
            delayMembership["normal"],
        ),
        ctrl.Rule(
            airTemperatureMember["hot"]
            & humidityMember["moist"]
            & waterTemperatureMember["hot"],
            delayMembership["normal"],
        ),
    ]

    sprayingDelayCtrl = ctrl.ControlSystem(rules)
    sprayingDelay = ctrl.ControlSystemSimulation(sprayingDelayCtrl)

    sprayingDelay.input["Air Temperature (°C)"] = airTemperature
    sprayingDelay.input["Humidity (%)"] = humidity
    sprayingDelay.input["Water Temperature (°C)"] = waterTemperature

    sprayingDelay.compute()

    # Return result as Decimal
    return int(np.round(sprayingDelay.output["Delay (minutes)"], 0))
