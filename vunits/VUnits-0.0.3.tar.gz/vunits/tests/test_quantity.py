import os
import unittest
import math

from vunits.quantity import Quantity, _force_get_quantity, _return_quantity

class TestQuantityModule(unittest.TestCase):
    def test_force_get_quantity(self):
        vel1 = Quantity(mag=10., m=1., s=-1.)
        self.assertEqual(_force_get_quantity(vel1), vel1)
        self.assertEqual(_force_get_quantity(vel1, 'm/s'), vel1)

    def test_return_quantity(self):
        vel1 = Quantity(mag=10., m=1., s=-1.)
        self.assertEqual(_return_quantity(vel1, True), vel1)
        self.assertEqual(_return_quantity(vel1, False, 'm/s'), vel1.mag)
        self.assertEqual(_return_quantity(vel1, False, 'cm/s'), vel1.mag*100.)

class TestQuantityClass(unittest.TestCase):
    def setUp(self):
        self.mag1 = 12.3456
        self.mag2 = 5.
        self.vel1 = Quantity(mag=self.mag1, m=1., s=-1.)
        self.vel2 = Quantity(mag=self.mag2, m=1., s=-1.)
        self.accel1 = Quantity(mag=10., m=1., s=-2)

    def test_neg(self):
        self.assertEqual(-self.vel1, Quantity(mag=-self.mag1, m=1., s=-1.))

    def test_abs(self):
        self.assertEqual(abs(self.vel1), Quantity(mag=self.mag1, m=1., s=-1.))

    def test_round(self):
        n = 5
        self.assertEqual(round(self.vel1, n),
                         Quantity(mag=round(self.mag1, n), m=1., s=-1.))

    def test_floor(self):
        self.assertEqual(math.floor(self.vel1),
                         Quantity(mag=math.floor(self.mag1), m=1., s=-1.))

    def test_ceil(self):
        self.assertEqual(math.ceil(self.vel1),
                         Quantity(mag=math.ceil(self.mag1), m=1., s=-1.))

    def test_trunc(self):
        self.assertEqual(math.trunc(self.vel1),
                         Quantity(mag=math.trunc(self.mag1), m=1., s=-1.))

    def test_iadd(self):
        # Set up the class to use
        mag3 = 5.
        vel3 = Quantity(mag=mag3, m=1., s=-1.)

        # Test with another Quantity object of similar units
        vel3 += self.vel1
        self.assertEqual(vel3, Quantity(mag=self.mag1+mag3, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 += 1.
        with self.assertRaises(TypeError):
            vel3 += Quantity(mag=1., kg=1.)

    def test_isub(self):
        # Set up the class to use
        mag3 = 5.
        vel3 = Quantity(mag=mag3, m=1., s=-1.)

        # Test with another Quantity object of similar units
        vel3 -= self.vel1
        self.assertEqual(vel3, Quantity(mag=mag3-self.mag1, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 -= 1.
        with self.assertRaises(TypeError):
            vel3 -= Quantity(mag=1., kg=1.)

    def test_imul(self):
        # Set up the class to use
        mag3 = 5.
        vel3 = Quantity(mag=mag3, m=1., s=-1.)

        # Test with another Quantity object of similar units
        vel3 *= self.vel1
        self.assertEqual(vel3, Quantity(mag=mag3*self.mag1, m=2., s=-2.))

        mag4 = 10.
        vel4 = Quantity(mag=mag4, m=1., s=-1.)
        vel4 *= 2.
        self.assertEqual(vel4, Quantity(mag=mag4*2., m=1., s=-1.))

    def test_int(self):
        self.assertEqual(int(self.vel1), int(self.mag1))

    def test_float(self):
        self.assertEqual(float(self.vel1), float(self.mag1))

    def test_str(self):
        self.assertEqual(str(self.vel1),
                         '{} m s^-1'.format(self.mag1))

    def test_add(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel1 + self.vel2
        self.assertEqual(vel3, Quantity(mag=self.mag1+self.mag2, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 = self.vel1 + 1.
        with self.assertRaises(TypeError):
            vel3 = self.vel1 + Quantity(mag=1., kg=1.)

    def test_radd(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel2 + self.vel1
        self.assertEqual(vel3, Quantity(mag=self.mag1+self.mag2, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 = 1. + self.vel1
        with self.assertRaises(TypeError):
            vel3 = Quantity(mag=1., kg=1.) + self.vel1

    def test_sub(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel1 - self.vel2
        self.assertEqual(vel3, Quantity(mag=self.mag1-self.mag2, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 = self.vel1 - 1.
        with self.assertRaises(TypeError):
            vel3 = self.vel1 - Quantity(mag=1., kg=1.)

    def test_rsub(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel2 - self.vel1
        self.assertEqual(vel3, Quantity(mag=self.mag2-self.mag1, m=1., s=-1))

        # Test if error raised when using incompatible units
        with self.assertRaises(TypeError):
            vel3 = 1. - self.vel1
        with self.assertRaises(TypeError):
            vel3 = Quantity(mag=1., kg=1.) - self.vel1

    def test_mul(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel1 * self.vel2
        self.assertEqual(vel3, Quantity(mag=self.mag2*self.mag1, m=2., s=-2.))

        vel4 = self.vel1 * 2.
        self.assertEqual(vel4, Quantity(mag=self.mag1*2., m=1., s=-1.))

    def test_rmul(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel2 * self.vel1
        self.assertEqual(vel3, Quantity(mag=self.mag2*self.mag1, m=2., s=-2.))

        vel4 = 2.*self.vel1
        self.assertEqual(vel4, Quantity(mag=self.mag1*2., m=1., s=-1.))

    def test_floordiv(self):
        # Test with another Quantity object of similar units
        time1 = self.vel1 // self.accel1
        self.assertEqual(time1,
                         Quantity(mag=self.mag1 // self.accel1.mag, s=1.))

        vel3 = self.vel1 // 2.
        self.assertEqual(vel3, Quantity(mag=self.mag1 // 2., m=1., s=-1.))

    def test_rfloordiv(self):
        # Test with another Quantity object of similar units
        time1 = self.vel1 // self.accel1
        self.assertEqual(time1,
                         Quantity(mag=self.mag1 // self.accel1.mag, s=1.))

        vel3 = 2 // self.vel1
        self.assertEqual(vel3, Quantity(mag=2 // self.mag1, m=-1., s=1.))

    def test_truediv(self):
        # Test with another Quantity object of similar units
        time1 = self.vel1 / self.accel1
        self.assertEqual(time1,
                         Quantity(mag=self.mag1 / self.accel1.mag, s=1.))

        vel3 = self.vel1 / 2.
        self.assertEqual(vel3, Quantity(mag=self.mag1 / 2., m=1., s=-1.))

    def test_rtruediv(self):
        # Test with another Quantity object of similar units
        time1 = self.vel1 / self.accel1
        self.assertEqual(time1,
                         Quantity(mag=self.mag1 / self.accel1.mag, s=1.))

        inv_vel1 = 2 / self.vel1
        self.assertEqual(inv_vel1, Quantity(mag=2 / self.mag1, m=-1., s=1.))

    def test_pow(self):
        # Test with another Quantity object of similar units
        vel3 = self.vel1 ** 2
        self.assertEqual(vel3, Quantity(mag=self.mag1**2, m=2., s=-2.))

        vel4 = self.vel1 ** Quantity(2.)
        self.assertEqual(vel4, Quantity(mag=self.mag1**2., m=2., s=-2.))

        with self.assertRaises(TypeError):
            self.vel1 ** self.vel2

    def test_lt(self):
        self.assertTrue(self.vel2 < self.vel1)
        self.assertFalse(self.vel1 < self.vel2)
        with self.assertRaises(TypeError):
            self.vel2 < self.accel1            
        with self.assertRaises(TypeError):
            self.vel2 < 1.

    def test_le(self):
        self.assertTrue(self.vel2 <= self.vel1)
        self.assertTrue(self.vel2 <= self.vel2)
        self.assertFalse(self.vel1 <= self.vel2)
        with self.assertRaises(TypeError):
            self.vel2 <= self.accel1            
        with self.assertRaises(TypeError):
            self.vel2 <= 1.

    def test_eq(self):
        self.assertTrue(self.vel1 == self.vel1)
        self.assertFalse(self.vel1 == self.vel2)
        self.assertFalse(self.vel2 == self.accel1)
        self.assertFalse(self.vel2 == 1.)

    def test_ne(self):
        self.assertFalse(self.vel1 != self.vel1)
        self.assertTrue(self.vel1 != self.vel2)
        self.assertTrue(self.vel2 != self.accel1)
        self.assertTrue(self.vel2 != 1.)

    def test_gt(self):
        self.assertTrue(self.vel1 > self.vel2)
        self.assertFalse(self.vel2 > self.vel1)
        with self.assertRaises(TypeError):
            self.vel2 > self.accel1            
        with self.assertRaises(TypeError):
            self.vel2 > 1.

    def test_ge(self):
        self.assertTrue(self.vel1 >= self.vel2)
        self.assertTrue(self.vel1 >= self.vel1)
        self.assertFalse(self.vel2 >= self.vel1)
        with self.assertRaises(TypeError):
            self.vel2 > self.accel1            
        with self.assertRaises(TypeError):
            self.vel2 > 1.

    def test_is_dimless(self):
        self.assertTrue(Quantity(mag=1.)._is_dimless())
        self.assertFalse(self.vel1._is_dimless())

    def test_is_temp(self):
        self.assertTrue(Quantity(mag=1., K=1.)._is_temp())
        self.assertFalse(Quantity(mag=1., K=-1.)._is_temp())
        self.assertFalse(Quantity(mag=1., kg=1., K=1.)._is_temp())
        self.assertFalse(Quantity(mag=1.)._is_temp())
        self.assertFalse(self.vel1._is_temp())

    def test_get_other_units(self):
        self.assertTrue(self.vel2.units.equals(
                self.vel1._get_other_units(self.vel2)))
        self.assertIsNone(self.vel1._get_other_units(1))

    def test_call(self):
        self.assertAlmostEqual(self.vel1(), self.mag1)
        self.assertAlmostEqual(self.vel1('cm/s'), self.mag1*100.)
        self.assertAlmostEqual(self.vel1('cm/min'), self.mag1*100.*60.)
        with self.assertRaises(ValueError):
            self.vel1('cm3')
        
        temp = Quantity(mag=273.15, K=1.)
        self.assertEqual(temp('oC'), temp.mag-273.15)

    def test_from_units(self):
        self.assertEqual(Quantity.from_units(mag=self.mag1, units='m/s'),
                         self.vel1)
        self.assertEqual(Quantity.from_units(mag=self.mag1, units='m s-1'),
                         self.vel1)
        self.assertEqual(Quantity.from_units(mag=self.mag1, units='m s^-1'),
                         self.vel1)
        self.assertEqual(Quantity.from_units(mag=self.accel1.mag, units='m/s2'),
                         self.accel1)

    def test_from_qty(self):
        self.assertEqual(Quantity._from_qty(mag=self.mag1,
                                            units=self.vel1.units),
                         self.vel1)
                         

if __name__ == '__main__':
    unittest.main()