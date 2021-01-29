import time
from typing import Callable

from .vec import *
from .objects import *
from .image import Image


class Raymarcher:

    def __init__(self, scene: Base):
        self.scene = scene
        self.default_material = Color((.5, .5, .5))
        self.background_color = Vec3()
        self.max_reflections = 5
        self.statistics = Statistics()

    def render(
            self,
            image: Image,
            ray_function: Callable,
            aa: int = 0,
            verbose: bool = True,
    ):
        self.statistics = Statistics()
        self.statistics.start_time = time.time()
        self.statistics.aa = aa
        self.statistics.num_pixels = image.width * image.height
        self.statistics.progress_time = time.time()

        aa = max(1, aa)

        for y in range(image.height * aa):
            norm_y = (y / max(1, image.height * aa - 1) - .5) * -2.
            for x in range(image.width * aa):
                norm_x = (x / max(1, image.width * aa - 1) - .5) * 2.

                origin, direction = ray_function(Vec2(norm_x, norm_y))
                col = self._get_ray_color(origin, direction, self.max_reflections)
                image.data[y // aa][x // aa] += col

                self.statistics.num_pixel_casts += 1

                if verbose:
                    ti = time.time()
                    if ti - self.statistics.progress_time >= 1.:
                        self.statistics._dump_verbose(ti)

        if aa > 1:
            fac = 1. / (aa * aa)
            image.map(lambda c: c * fac)

        self.statistics.end_time = time.time()

    def _get_ray_color(self, origin: Vec3, direction: Vec3, max_reflections: int, ignore_objects=None):
        pos, obj = self.scene.raymarch(origin, direction, ignore_objects=ignore_objects)
        self.statistics.num_rays += 1

        if obj:
            return self._get_object_color(obj, pos, direction, max_reflections)

        return self.background_color

    def _get_object_color(
            self,
            obj: Base,
            global_pos: Vec3,
            ray_direction: Vec3,
            max_reflections: int,
    ):

        local_pos = obj.global_to_local_position(global_pos)

        material = getattr(obj, "material", None)
        if material is None:
            material = self.default_material

        color_sum = Vec3()
        amt_sum = 0.
        for m, amt in material.materials(local_pos):

            color = getattr(m, "color", None)
            if color is not None:
                color_sum += color
                amt_sum += amt

            reflective = getattr(m, "reflective", None)
            if reflective and max_reflections > 0:
                color = self._get_reflect_ray_color(
                    obj, global_pos, local_pos, ray_direction, max_reflections - 1
                )
                color_sum += color
                amt_sum += reflective

        if amt_sum:
            color_sum /= amt_sum

        return color_sum

    def _get_reflect_ray_color(
            self,
            obj: Base,
            global_pos: Vec3,
            local_pos: Vec3,
            ray_direction: Vec3,
            max_reflections: int,
    ):
        self.statistics.num_reflections += 1

        normal = self.scene.normal(global_pos)
        direction = ray_direction.reflected(normal)
        return self._get_ray_color(
            local_pos,
            direction,
            max_reflections=max_reflections,
            ignore_objects={obj},
        )



class Statistics:

    def __init__(self):
        self.start_time = 0.
        self.end_time = 0.
        self.progress_time = 0.
        self.last_progress_time = 0.
        self.last_num_pixel_casts = 0
        self.num_rays = 0
        self.num_pixels = 0
        self.num_pixel_casts = 0
        self.num_reflections = 0
        self.aa = 1

    def dump(self):
        num_pix = max(1, self.num_pixels)
        seconds = self.end_time - self.start_time
        per_sec = 0. if not seconds else 1. / seconds

        print(f"render time           : {seconds:0.2f} sec")
        print(f"number of rays        : {self.num_rays}"
              f", {self.num_rays / num_pix:0.2f}/pixel"
              f", {self.num_rays * per_sec:0.2f}/sec")
        print(f"number of reflections : {self.num_reflections}"
              f", {self.num_reflections / num_pix:0.3f}/pixel")

    def _dump_verbose(self, ti: float):
        self.last_progress_time = self.progress_time
        self.progress_time = ti

        max_pixels = self.num_pixels * self.aa ** 2
        progress = self.num_pixel_casts / max_pixels * 100
        elapsed_seconds = max(0.0001, ti - self.start_time)

        rays_per_second = self.num_rays / elapsed_seconds

        print(
            f"\r{progress:0.2f}%"
            f" elapsed: {elapsed_seconds:0.2f}sec"
            f" rays/sec: {rays_per_second:0.2f}\r",
            end="",
        )

        self.last_num_pixel_casts = self.num_pixel_casts
