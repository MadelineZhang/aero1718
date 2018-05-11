# this script calculates the antenna pole height required for USC2018 competition
import math


class FresnelZoneCalculator:
    def __init__(self, distance, frequency, area_percentage):
        self.d = distance
        self.f = frequency
        self.r = 17.32 * math.sqrt(self.d/(4*self.f)) # here d is in km
        self.ap = area_percentage
        self.ellipse = math.pi * self.r * (self.d / 2) * self.ap
        self.h = self.r
        self.angle = math.degrees(math.atan(self.r * self.ap/(1000 * self.d / 2)))
        self.H = self.d * 1000 * math.sin(math.radians(self.angle))

    def height_clearance(self):
        ground_blockage = (self.ellipse * self.ap)/4 - self.r * self.d / 4
        blockage_ratio = ground_blockage / (self.ellipse * self.ap)
        height = ("%.2f" % round(self.H, 2))
        clearance = ("%.2f" % round((self.ap - blockage_ratio) * 100, 2))
        return height, clearance, self.ap


def main():
    calculator = FresnelZoneCalculator(1, 5.8, 0.8)
    height, clearance, percentage = calculator.height_clearance()
    print('antenna pole height for '+str(clearance)+'% clearance: '+str(height)+' m')

main()




