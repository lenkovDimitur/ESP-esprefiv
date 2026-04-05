"""Caches the last rotozoom result for a needle sprite.

Avoids re-computing rotozoom when the gauge value hasn't changed between frames.
Each gauge gets its own NeedleCache instance.
"""

import pygame


class NeedleCache:
    """Caches the last rotated needle surface and angle."""

    def __init__(self, master_sprite):
        """
        Args:
            master_sprite: Pre-rendered pygame Surface with needle pointing RIGHT,
                           pivot at Surface center.
        """
        self._master = master_sprite
        self._last_angle = None
        self._cached_surf = None
        self._cached_rect = None

    def get_rotated(self, angle_deg, pivot_pos):
        """Get the rotated needle surface and its blit rect.

        Args:
            angle_deg: Rotation angle in degrees (CCW from east, math convention).
            pivot_pos: (x, y) screen position of the gauge center / needle pivot.

        Returns:
            (surface, rect) — ready to blit.
        """
        if angle_deg != self._last_angle:
            self._last_angle = angle_deg
            self._cached_surf = pygame.transform.rotozoom(
                self._master, angle_deg, 1.0)
            self._cached_rect = self._cached_surf.get_rect(center=pivot_pos)
        else:
            # Angle unchanged, but pivot might have moved (unlikely)
            self._cached_rect = self._cached_surf.get_rect(center=pivot_pos)

        return self._cached_surf, self._cached_rect
