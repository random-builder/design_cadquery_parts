__all__ = [
    'display_environments',
    'map_environment',
    'DisplayEnvironment',
]

import logging
log = logging.getLogger(__name__)


display_environments = set()


def map_environment(**kwargs):
    def inner(cls):
        disp_env = cls(**kwargs)
        # is already mappped?
        try:
            i = display_environments.index(disp_env)  # raises ValueError
            # report duplicate
            raise RuntimeError(
                ("environment %r already mapped, " % display_environments[i]) +
                ("can't map duplicate %r" % disp_env)
            )
        except ValueError:
            pass  # as expected
        # map class
        display_environments = sorted(display_environments + [disp_env])

        return cls
    return inner


class DisplayEnvironment(object):
    def __init__(self, name, order, condition):
        self.name = name
        self.order = order
        self.condition = condition

    def __repr__(self):
        return "<{cls}: {name}, {order}>".format(
            cls=type(self).__name__,
            name=self.name,
            order=self.order,
        )

    def __lt__(self, other):
        return self.order < other.order

    def __eq__(self, other):
        return self.name == other.name

    def display(self, *args, **kwargs):
        return self.display_callback(self, *args, **kwargs)

    def display_callback(self, *args, **kwargs):
        """
        Display given component in this environment.

        .. note::

            To be overridden by inheriting classes

        An example of a introducing a custom display environment.

        .. doctest::

            import cqparts
            from cqparts.display import DisplayEnvironment

            def is_text_env():
                # function that returns True if it's run in the
                # desired environment.
                import sys
                # Python 2.x
                if sys.version_info[0] == 2:
                    return isinstance(sys.stdout, file)
                # Python 3.x
                import io
                return isinstance(sys.stdout, io.TextIOWrapper)

            @map_environment(
                name="text",
                order=0,  # force display to be first priority
                condition=is_text_env,
            )
            class TextDisplay(DisplayEnvironment):
                def display_callback(self, component, **kwargs):
                    # Print component details to STDOUT
                    if isinstance(component, cqparts.Assembly):
                        sys.stdout.write(component.tree_str(add_repr=True))
                    else:  # assumed to be a cqparts.Part
                        sys.stdout.write("%r\\n" % (component))

        ``is_text_env()`` checks if there's a valid ``sys.stdout`` to write to,
        ``TextDisplay`` defines how to display any given component,
        and the ``@map_environment`` decorator adds the display paired with
        its environment test function.

        When using :meth:`display() <cqparts.display.display>`, this display
        will be used if ``is_text_env()`` returns ``True``, and no previously
        mapped environment with a smaller ``order`` tested ``True``:

        .. doctest::

            # create component to display
            from cqparts_misc.basic.primatives import Cube
            cube = Cube()

            # display component
            from cqparts.display import display
            display(cube)

        The ``display_callback`` will be called via
        :meth:`display() <DisplayEnvironment.display>`.  So to call this
        display method directly:

        .. doctest::

            TextDisplay.display(cube)

        :raises: NotImplementedError if not overridden
        """
        if type(self) is DisplayEnvironment:
            raise RuntimeError(
                ("%r is not a functional display environment, " % (type(self))) +
                "it's meant to be inherited by an implemented environment"
            )
        raise NotImplementedError(
            "display_callback function not overridden by %r" % (type(self))
        )
