from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType
import copy as _copy


class Z(_BaseTraceHierarchyType):

    # fill
    # ----
    @property
    def fill(self):
        """
        Sets the fill ratio of the `slices`. The default fill value of
        the `slices` is 1 meaning that they are entirely shaded. On the
        other hand Applying a `fill` ratio less than one would allow
        the creation of openings parallel to the edges.
    
        The 'fill' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self["fill"]

    @fill.setter
    def fill(self, val):
        self["fill"] = val

    # locations
    # ---------
    @property
    def locations(self):
        """
        Specifies the location(s) of slices on the axis. When not
        specified slices would be created for all points of the axis z
        except start and end.
    
        The 'locations' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self["locations"]

    @locations.setter
    def locations(self, val):
        self["locations"] = val

    # locationssrc
    # ------------
    @property
    def locationssrc(self):
        """
        Sets the source reference on plot.ly for  locations .
    
        The 'locationssrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self["locationssrc"]

    @locationssrc.setter
    def locationssrc(self, val):
        self["locationssrc"] = val

    # show
    # ----
    @property
    def show(self):
        """
        Determines whether or not slice planes about the z dimension
        are drawn.
    
        The 'show' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self["show"]

    @show.setter
    def show(self, val):
        self["show"] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return "isosurface.slices"

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis z except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the z
            dimension are drawn.
        """

    def __init__(
        self,
        arg=None,
        fill=None,
        locations=None,
        locationssrc=None,
        show=None,
        **kwargs
    ):
        """
        Construct a new Z object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.isosurface.slices.Z
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis z except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the z
            dimension are drawn.

        Returns
        -------
        Z
        """
        super(Z, self).__init__("z")

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = _copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.isosurface.slices.Z 
constructor must be a dict or 
an instance of plotly.graph_objs.isosurface.slices.Z"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop("skip_invalid", False)

        # Import validators
        # -----------------
        from plotly.validators.isosurface.slices import z as v_z

        # Initialize validators
        # ---------------------
        self._validators["fill"] = v_z.FillValidator()
        self._validators["locations"] = v_z.LocationsValidator()
        self._validators["locationssrc"] = v_z.LocationssrcValidator()
        self._validators["show"] = v_z.ShowValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop("fill", None)
        self["fill"] = fill if fill is not None else _v
        _v = arg.pop("locations", None)
        self["locations"] = locations if locations is not None else _v
        _v = arg.pop("locationssrc", None)
        self["locationssrc"] = locationssrc if locationssrc is not None else _v
        _v = arg.pop("show", None)
        self["show"] = show if show is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False


from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType
import copy as _copy


class Y(_BaseTraceHierarchyType):

    # fill
    # ----
    @property
    def fill(self):
        """
        Sets the fill ratio of the `slices`. The default fill value of
        the `slices` is 1 meaning that they are entirely shaded. On the
        other hand Applying a `fill` ratio less than one would allow
        the creation of openings parallel to the edges.
    
        The 'fill' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self["fill"]

    @fill.setter
    def fill(self, val):
        self["fill"] = val

    # locations
    # ---------
    @property
    def locations(self):
        """
        Specifies the location(s) of slices on the axis. When not
        specified slices would be created for all points of the axis y
        except start and end.
    
        The 'locations' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self["locations"]

    @locations.setter
    def locations(self, val):
        self["locations"] = val

    # locationssrc
    # ------------
    @property
    def locationssrc(self):
        """
        Sets the source reference on plot.ly for  locations .
    
        The 'locationssrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self["locationssrc"]

    @locationssrc.setter
    def locationssrc(self, val):
        self["locationssrc"] = val

    # show
    # ----
    @property
    def show(self):
        """
        Determines whether or not slice planes about the y dimension
        are drawn.
    
        The 'show' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self["show"]

    @show.setter
    def show(self, val):
        self["show"] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return "isosurface.slices"

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis y except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the y
            dimension are drawn.
        """

    def __init__(
        self,
        arg=None,
        fill=None,
        locations=None,
        locationssrc=None,
        show=None,
        **kwargs
    ):
        """
        Construct a new Y object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.isosurface.slices.Y
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis y except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the y
            dimension are drawn.

        Returns
        -------
        Y
        """
        super(Y, self).__init__("y")

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = _copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.isosurface.slices.Y 
constructor must be a dict or 
an instance of plotly.graph_objs.isosurface.slices.Y"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop("skip_invalid", False)

        # Import validators
        # -----------------
        from plotly.validators.isosurface.slices import y as v_y

        # Initialize validators
        # ---------------------
        self._validators["fill"] = v_y.FillValidator()
        self._validators["locations"] = v_y.LocationsValidator()
        self._validators["locationssrc"] = v_y.LocationssrcValidator()
        self._validators["show"] = v_y.ShowValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop("fill", None)
        self["fill"] = fill if fill is not None else _v
        _v = arg.pop("locations", None)
        self["locations"] = locations if locations is not None else _v
        _v = arg.pop("locationssrc", None)
        self["locationssrc"] = locationssrc if locationssrc is not None else _v
        _v = arg.pop("show", None)
        self["show"] = show if show is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False


from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType
import copy as _copy


class X(_BaseTraceHierarchyType):

    # fill
    # ----
    @property
    def fill(self):
        """
        Sets the fill ratio of the `slices`. The default fill value of
        the `slices` is 1 meaning that they are entirely shaded. On the
        other hand Applying a `fill` ratio less than one would allow
        the creation of openings parallel to the edges.
    
        The 'fill' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self["fill"]

    @fill.setter
    def fill(self, val):
        self["fill"] = val

    # locations
    # ---------
    @property
    def locations(self):
        """
        Specifies the location(s) of slices on the axis. When not
        specified slices would be created for all points of the axis x
        except start and end.
    
        The 'locations' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self["locations"]

    @locations.setter
    def locations(self, val):
        self["locations"] = val

    # locationssrc
    # ------------
    @property
    def locationssrc(self):
        """
        Sets the source reference on plot.ly for  locations .
    
        The 'locationssrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self["locationssrc"]

    @locationssrc.setter
    def locationssrc(self, val):
        self["locationssrc"] = val

    # show
    # ----
    @property
    def show(self):
        """
        Determines whether or not slice planes about the x dimension
        are drawn.
    
        The 'show' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self["show"]

    @show.setter
    def show(self, val):
        self["show"] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return "isosurface.slices"

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis x except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the x
            dimension are drawn.
        """

    def __init__(
        self,
        arg=None,
        fill=None,
        locations=None,
        locationssrc=None,
        show=None,
        **kwargs
    ):
        """
        Construct a new X object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.isosurface.slices.X
        fill
            Sets the fill ratio of the `slices`. The default fill
            value of the `slices` is 1 meaning that they are
            entirely shaded. On the other hand Applying a `fill`
            ratio less than one would allow the creation of
            openings parallel to the edges.
        locations
            Specifies the location(s) of slices on the axis. When
            not specified slices would be created for all points of
            the axis x except start and end.
        locationssrc
            Sets the source reference on plot.ly for  locations .
        show
            Determines whether or not slice planes about the x
            dimension are drawn.

        Returns
        -------
        X
        """
        super(X, self).__init__("x")

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = _copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.isosurface.slices.X 
constructor must be a dict or 
an instance of plotly.graph_objs.isosurface.slices.X"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop("skip_invalid", False)

        # Import validators
        # -----------------
        from plotly.validators.isosurface.slices import x as v_x

        # Initialize validators
        # ---------------------
        self._validators["fill"] = v_x.FillValidator()
        self._validators["locations"] = v_x.LocationsValidator()
        self._validators["locationssrc"] = v_x.LocationssrcValidator()
        self._validators["show"] = v_x.ShowValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop("fill", None)
        self["fill"] = fill if fill is not None else _v
        _v = arg.pop("locations", None)
        self["locations"] = locations if locations is not None else _v
        _v = arg.pop("locationssrc", None)
        self["locationssrc"] = locationssrc if locationssrc is not None else _v
        _v = arg.pop("show", None)
        self["show"] = show if show is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False
