# -*- coding: utf-8 -*-
"""Panel for PhononWorkchain plugin.

Authors:

    * Miki Bonacci <miki.bonacci@psi.ch>
    Inspired by Xing Wang <xing.wang@psi.ch>
"""
import ipywidgets as ipw
from aiida.orm import Float, Int, Str

from aiidalab_qe.common.panel import Panel
from aiida_vibroscopy.common.properties import PhononProperty


class Setting(Panel):
    title = "Vibrational Settings"

    def __init__(self, **kwargs):
        self.settings_title = ipw.HTML(
            """<div style="padding-top: 0px; padding-bottom: 0px">
            <h4>Phonons and dielectric settings</h4></div>"""
        )
        self.settings_help = ipw.HTML(
            """<div style="line-height: 140%; padding-top: 0px; padding-bottom: 5px">
            Please select the phononic and dielectric properties to be computed in the simulation. Usually,
            supercell size of 2x2x2 is at convergence with respect to finite atomic displacement in the unit cell.
            </div>"""
        )
        
        self.polar_help = ipw.HTML(
            """<div style="line-height: 140%; padding-top: 5px; padding-bottom: 5px">
            If the material is polar, more 
            accurate phonon properties interpolation is performed.
            </div>"""
        )
        
        self.workchain_protocol = ipw.ToggleButtons(
            options=["fast", "moderate", "precise"],
            value="moderate",
        )
        
        #I want to be able to select more than only one... this has to change at the PhononWorkChain level.
        self.phonon_property = ipw.Dropdown(
            options=[
                ["band structure","BANDS"], 
                ["density of states (DOS)","DOS"], 
                ["thermal properties","THERMODYNAMIC"],
                ["force constants","NONE"],
                ["none","none"]
            ],
            value="BANDS",
            description="Phonon property:",
            disabled=False,
            style={"description_width": "initial"},
        )
        
        self.dielectric_property = ipw.Dropdown(
            options=[
                ["dielectric tensor","dielectric"], 
                ["infrared","ir"], 
                ["raman",'raman'], 
                ['born-charges',"born-charges"], 
                #'nac', 
                #'bec', 
                #'susceptibility-derivative',
                #'non-linear-susceptibility',
                ['none','none'],
                ],
            value="none",
            description="Dielectric property:",
            disabled=False,
            style={"description_width": "initial"},
        )

        self.spectrum = ipw.ToggleButtons(
            options=[("Off","off"),("Infrared", "ir"), ("Raman", "raman")],
            value="off",
            style={"description_width": "initial"},
        )
        
        # 1. Supercell
        self.supercell=[1,1,1]
        def change_supercell(_=None):
            self.supercell = [
                _supercell[0].value,
                _supercell[1].value,
                _supercell[2].value,
            ]

        _supercell = [
            ipw.BoundedIntText(value=2, min=1, layout={"width": "40px"}),
            ipw.BoundedIntText(value=2, min=1, layout={"width": "40px"}),
            ipw.BoundedIntText(value=2, min=1, layout={"width": "40px"}),
        ]
        for elem in _supercell:
            elem.observe(change_supercell, names="value")
        self.supercell_selector = ipw.HBox(
            children=[ipw.HTML(description="Supercell size:",style={"description_width": "initial"})] + _supercell,
        )
        
        #to trigger Dielectric property = Raman... FOR POLAR MATERIALS. 
        self.material_is_polar = ipw.ToggleButtons(
            options=[("Off", "off"), ("On", "on")],
            value="off",
            style={"description_width": "initial"},
        )

        self.children = [
            self.settings_title,
            self.settings_help,
            ipw.HBox(
                children=[
                    ipw.Label(
                        "Spectroscopy:",
                        layout=ipw.Layout(justify_content="flex-start", width="120px"),
                    ),
                    self.spectrum,
                ]
            ),
            ipw.HBox(
                children=[
                    self.phonon_property,
                    self.supercell_selector,
                    ],
                layout=ipw.Layout(justify_content="flex-start"),
            ),
            self.dielectric_property,
            self.polar_help,
            ipw.HBox(
                children=[
                    ipw.Label(
                        "Material is polar:",
                        layout=ipw.Layout(justify_content="flex-start", width="120px"),
                    ),
                    self.material_is_polar,
                ]
            ),
        ]
        super().__init__(**kwargs)

    def get_panel_value(self):
        """Return a dictionary with the input parameters for the plugin."""
        if isinstance(self.phonon_property,str):
            return {
                "phonon_property": self.phonon_property,
                "dielectric_property": self.dielectric_property,
                "material_is_polar": self.material_is_polar,
                "supercell_selector": self.supercell,
                "spectrum": self.spectrum,
                }
        return {
                "phonon_property": self.phonon_property.value,
                "dielectric_property": self.dielectric_property.value,
                "material_is_polar": self.material_is_polar.value,
                "supercell_selector": self.supercell,
                "spectrum": self.spectrum.value,
                }

    def load_panel_value(self, input_dict):
        """Load a dictionary with the input parameters for the plugin."""
        self.phonon_property.value = input_dict.get("phonon_property","none")
        self.dielectric_property.value = input_dict.get("dielectric_property", "none")
        self.material_is_polar.value = input_dict.get("material_is_polar", "off")
        self.spectrum.value = input_dict.get("spectrum", "off")
        self.supercell = input_dict.get("supercell_selector", [2,2,2])
