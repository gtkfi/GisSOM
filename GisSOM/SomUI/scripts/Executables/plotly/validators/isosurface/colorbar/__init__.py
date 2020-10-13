import _plotly_utils.basevalidators


class YpadValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="ypad", parent_name="isosurface.colorbar", **kwargs):
        super(YpadValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class YanchorValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="yanchor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(YanchorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["top", "middle", "bottom"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class YValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="y", parent_name="isosurface.colorbar", **kwargs):
        super(YValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            max=kwargs.pop("max", 3),
            min=kwargs.pop("min", -2),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class XpadValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="xpad", parent_name="isosurface.colorbar", **kwargs):
        super(XpadValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class XanchorValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="xanchor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(XanchorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["left", "center", "right"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class XValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="x", parent_name="isosurface.colorbar", **kwargs):
        super(XValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            max=kwargs.pop("max", 3),
            min=kwargs.pop("min", -2),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TitleValidator(_plotly_utils.basevalidators.TitleValidator):
    def __init__(
        self, plotly_name="title", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TitleValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Title"),
            data_docs=kwargs.pop(
                "data_docs",
                """
            font
                Sets this color bar's title font. Note that the
                title's font used to be set by the now
                deprecated `titlefont` attribute.
            side
                Determines the location of color bar's title
                with respect to the color bar. Note that the
                title's location used to be set by the now
                deprecated `titleside` attribute.
            text
                Sets the title of the color bar. Note that
                before the existence of `title.text`, the
                title's contents used to be defined as the
                `title` attribute itself. This behavior has
                been deprecated.
""",
            ),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickwidthValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="tickwidth", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickvalssrcValidator(_plotly_utils.basevalidators.SrcValidator):
    def __init__(
        self, plotly_name="tickvalssrc", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickvalssrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "none"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickvalsValidator(_plotly_utils.basevalidators.DataArrayValidator):
    def __init__(
        self, plotly_name="tickvals", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickvalsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "data"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TicktextsrcValidator(_plotly_utils.basevalidators.SrcValidator):
    def __init__(
        self, plotly_name="ticktextsrc", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TicktextsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "none"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TicktextValidator(_plotly_utils.basevalidators.DataArrayValidator):
    def __init__(
        self, plotly_name="ticktext", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TicktextValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "data"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TicksuffixValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(
        self, plotly_name="ticksuffix", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TicksuffixValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TicksValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="ticks", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TicksValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["outside", "inside", ""]),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickprefixValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(
        self, plotly_name="tickprefix", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickprefixValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickmodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="tickmode", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickmodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            implied_edits=kwargs.pop("implied_edits", {}),
            role=kwargs.pop("role", "info"),
            values=kwargs.pop("values", ["auto", "linear", "array"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class TicklenValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="ticklen", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TicklenValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickformatstopValidator(_plotly_utils.basevalidators.CompoundValidator):
    def __init__(
        self,
        plotly_name="tickformatstopdefaults",
        parent_name="isosurface.colorbar",
        **kwargs
    ):
        super(TickformatstopValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Tickformatstop"),
            data_docs=kwargs.pop(
                "data_docs",
                """
""",
            ),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickformatstopsValidator(_plotly_utils.basevalidators.CompoundArrayValidator):
    def __init__(
        self, plotly_name="tickformatstops", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickformatstopsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Tickformatstop"),
            data_docs=kwargs.pop(
                "data_docs",
                """
            dtickrange
                range [*min*, *max*], where "min", "max" -
                dtick values which describe some zoom level, it
                is possible to omit "min" or "max" value by
                passing "null"
            enabled
                Determines whether or not this stop is used. If
                `false`, this stop is ignored even within its
                `dtickrange`.
            name
                When used in a template, named items are
                created in the output figure in addition to any
                items the figure already has in this array. You
                can modify these items in the output figure by
                making your own item with `templateitemname`
                matching this `name` alongside your
                modifications (including `visible: false` or
                `enabled: false` to hide it). Has no effect
                outside of a template.
            templateitemname
                Used to refer to a named item in this array in
                the template. Named items from the template
                will be created even without a matching item in
                the input figure, but you can modify one by
                making an item with `templateitemname` matching
                its `name`, alongside your modifications
                (including `visible: false` or `enabled: false`
                to hide it). If there is no template or no
                matching item, this item will be hidden unless
                you explicitly show it with `visible: true`.
            value
                string - dtickformat for described zoom level,
                the same as "tickformat"
""",
            ),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickformatValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(
        self, plotly_name="tickformat", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickfontValidator(_plotly_utils.basevalidators.CompoundValidator):
    def __init__(
        self, plotly_name="tickfont", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickfontValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Tickfont"),
            data_docs=kwargs.pop(
                "data_docs",
                """
            color

            family
                HTML font family - the typeface that will be
                applied by the web browser. The web browser
                will only be able to apply a font if it is
                available on the system which it operates.
                Provide multiple font families, separated by
                commas, to indicate the preference in which to
                apply fonts if they aren't available on the
                system. The plotly service (at https://plot.ly
                or on-premise) generates images on a server,
                where only a select number of fonts are
                installed and supported. These include "Arial",
                "Balto", "Courier New", "Droid Sans",, "Droid
                Serif", "Droid Sans Mono", "Gravitas One", "Old
                Standard TT", "Open Sans", "Overpass", "PT Sans
                Narrow", "Raleway", "Times New Roman".
            size

""",
            ),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickcolorValidator(_plotly_utils.basevalidators.ColorValidator):
    def __init__(
        self, plotly_name="tickcolor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickcolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class TickangleValidator(_plotly_utils.basevalidators.AngleValidator):
    def __init__(
        self, plotly_name="tickangle", parent_name="isosurface.colorbar", **kwargs
    ):
        super(TickangleValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class Tick0Validator(_plotly_utils.basevalidators.AnyValidator):
    def __init__(
        self, plotly_name="tick0", parent_name="isosurface.colorbar", **kwargs
    ):
        super(Tick0Validator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            implied_edits=kwargs.pop("implied_edits", {"tickmode": "linear"}),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class ThicknessmodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="thicknessmode", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ThicknessmodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["fraction", "pixels"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class ThicknessValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="thickness", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ThicknessValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class ShowticksuffixValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="showticksuffix", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ShowticksuffixValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["all", "first", "last", "none"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class ShowtickprefixValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="showtickprefix", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ShowtickprefixValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["all", "first", "last", "none"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class ShowticklabelsValidator(_plotly_utils.basevalidators.BooleanValidator):
    def __init__(
        self, plotly_name="showticklabels", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ShowticklabelsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class ShowexponentValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="showexponent", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ShowexponentValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["all", "first", "last", "none"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class SeparatethousandsValidator(_plotly_utils.basevalidators.BooleanValidator):
    def __init__(
        self,
        plotly_name="separatethousands",
        parent_name="isosurface.colorbar",
        **kwargs
    ):
        super(SeparatethousandsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class OutlinewidthValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="outlinewidth", parent_name="isosurface.colorbar", **kwargs
    ):
        super(OutlinewidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class OutlinecolorValidator(_plotly_utils.basevalidators.ColorValidator):
    def __init__(
        self, plotly_name="outlinecolor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(OutlinecolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class NticksValidator(_plotly_utils.basevalidators.IntegerValidator):
    def __init__(
        self, plotly_name="nticks", parent_name="isosurface.colorbar", **kwargs
    ):
        super(NticksValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class LenmodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="lenmode", parent_name="isosurface.colorbar", **kwargs
    ):
        super(LenmodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "info"),
            values=kwargs.pop("values", ["fraction", "pixels"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class LenValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="len", parent_name="isosurface.colorbar", **kwargs):
        super(LenValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class ExponentformatValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="exponentformat", parent_name="isosurface.colorbar", **kwargs
    ):
        super(ExponentformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["none", "e", "E", "power", "SI", "B"]),
            **kwargs
        )


import _plotly_utils.basevalidators


class DtickValidator(_plotly_utils.basevalidators.AnyValidator):
    def __init__(
        self, plotly_name="dtick", parent_name="isosurface.colorbar", **kwargs
    ):
        super(DtickValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            implied_edits=kwargs.pop("implied_edits", {"tickmode": "linear"}),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class BorderwidthValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="borderwidth", parent_name="isosurface.colorbar", **kwargs
    ):
        super(BorderwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class BordercolorValidator(_plotly_utils.basevalidators.ColorValidator):
    def __init__(
        self, plotly_name="bordercolor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(BordercolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class BgcolorValidator(_plotly_utils.basevalidators.ColorValidator):
    def __init__(
        self, plotly_name="bgcolor", parent_name="isosurface.colorbar", **kwargs
    ):
        super(BgcolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )
