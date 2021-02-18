# Helper functions to handle transformations
def vector_multiply(vec1, const):
    vec = [0, 0]
    vec[0] = vec1[0] * const
    vec[1] = vec1[1] * const
    return vec


def vector_div_const(vec1, const):
    if const == 0:
        return vec1
    vec = [0, 0]
    vec[0] = vec1[0] / const
    vec[1] = vec1[1] / const
    return vec


def vector_add(vec1, vec2):
    vec = [0, 0]
    vec[0] = vec1[0] + vec2[0]
    vec[1] = vec1[1] + vec2[1]
    return vec


def vector_sub(vec1, vec2):
    vec = [0, 0]
    vec[0] = vec1[0] - vec2[0]
    vec[1] = vec1[1] - vec2[1]
    return vec


def vector_norm(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


# Behaviours: alignment/cohesion/separation and attacking/evading patterns


def align(self, rock_group):
    steer = [0, 0]
    total = 0
    average_vectors = [0, 0]
    for rock in rock_group:
        if dist(rock.pos, self.pos) < rock_vision:
            average_vectors = vector_add(average_vectors, rock.vel)
            total += 1
    if total > 0:
        average_vectors = vector_div_const(average_vectors, total)
        average_vectors = vector_multiply(vector_div_const(average_vectors, vector_norm(average_vectors)), 3)
        steer = vector_sub(average_vectors, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply((vector_div_const(steer, vector_norm(steer))), 2)
    return steer


def cohesion(self, rock_group):
    steer = [0, 0]
    total = 0
    center_of_mass = [0, 0]
    for rock in rock_group:
        if self != rock and dist(rock.pos, self.pos) < rock_vision:
            center_of_mass = vector_add(center_of_mass, rock.pos)
            total += 1
    if total > 0:
        center_of_mass = vector_div_const(center_of_mass, total)
        vec_to_com = vector_sub(center_of_mass, self.pos)
        if vector_norm(vec_to_com) > 0:
            vec_to_com = vector_multiply((vector_div_const(vec_to_com, vector_norm(vec_to_com))), 1)
        steer = vector_sub(vec_to_com, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply((vector_div_const(steer, vector_norm(steer))), 1)
    return steer


def separation(self, rock_group):
    steer = [0, 0]
    total = 0
    average_vectors = [0, 0]
    for rock in rock_group:
        distance = dist(rock.pos, self.pos)
        if self.pos != rock.pos and distance < rock_vision - 100:
            diff = vector_sub(self.pos, rock.pos)
            diff = vector_div_const(diff, distance)
            average_vectors = vector_add(average_vectors, diff)
            total += 1
    if total > 0:
        average_vectors = vector_div_const(average_vectors, total)
        if vector_norm(steer) > 0:
            average_vectors = vector_multiply(vector_div_const(average_vectors, vector_norm(steer)), 2)
        steer = vector_sub(average_vectors, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply(vector_div_const(steer, vector_norm(steer)), 2.5)
    return steer


def evade(self, rock_group):
    steer = [0, 0]
    total = 0
    average_vectors = [0, 0]
    for rock in rock_group:
        distance = dist(my_ship.pos, self.pos)
        if self.pos != rock.pos and distance < rock_vision + 50:
            diff = vector_sub(self.pos, my_ship.pos)
            diff = vector_div_const(diff, distance)
            average_vectors = vector_add(average_vectors, diff)
            total += 1
    if total > 0:
        average_vectors = vector_div_const(average_vectors, total)
        if vector_norm(steer) > 0:
            average_vectors = vector_multiply(vector_div_const(average_vectors, vector_norm(steer)), 2)
        steer = vector_sub(average_vectors, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply(vector_div_const(steer, vector_norm(steer)), 2.5)
    return steer


def evade_missiles(self, rock_group, missile_group):
    steer = [0, 0]
    total = 0
    average_vectors = [0, 0]
    for rock in rock_group:
        for missile in missile_group:
            distance = dist(missile.pos, self.pos)
            if self.pos != rock.pos and distance < rock_vision + 50:
                diff = vector_sub(self.pos, missile.pos)
                diff = vector_div_const(diff, distance)
                average_vectors = vector_add(average_vectors, diff)
                total += 1
    if total > 0:
        average_vectors = vector_div_const(average_vectors, total)
        if vector_norm(steer) > 0:
            average_vectors = vector_multiply(vector_div_const(average_vectors, vector_norm(steer)), 2)
        steer = vector_sub(average_vectors, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply(vector_div_const(steer, vector_norm(steer)), 2.5)
    return steer


def attack(self, rock_group):
    steer = [0, 0]
    total = 0
    center_of_mass = [0, 0]
    for rock in rock_group:
        if self != rock and dist(my_ship.pos, self.pos) < rock_vision:
            center_of_mass = vector_add(center_of_mass, my_ship.pos)
            total += 1
    if total > 0:
        center_of_mass = vector_div_const(center_of_mass, total)
        vec_to_com = vector_sub(center_of_mass, self.pos)
        if vector_norm(vec_to_com) > 0:
            vec_to_com = vector_multiply((vector_div_const(vec_to_com, vector_norm(vec_to_com))), 2)
        steer = vector_sub(vec_to_com, self.vel)
        if vector_norm(steer) > 2:
            steer = vector_multiply((vector_div_const(steer, vector_norm(steer))), 2)
    return steer


def apply_behaviour(self, rock_group):
    self.acc = [0, 0]
    separation = self.separation(rock_group)
    cohesion = self.cohesion(rock_group)
    alignment = self.align(rock_group)
    evasion = self.evade(rock_group)
    attack = self.attack(rock_group)
    dodge = self.evade_missiles(rock_group, missile_group)
    self.acc = vector_add(self.acc, alignment)
    self.acc = vector_add(self.acc, separation)
    self.acc = vector_add(self.acc, cohesion)
    self.acc = vector_add(self.acc, dodge)
    self.acc = vector_add(self.acc, evasion)
    # self.acc = vector_add(self.acc, attack)
