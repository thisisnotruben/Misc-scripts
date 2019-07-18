extends Node

static func get_normal_point(p, v1, v2):
	var ab = (v2 - v1).normalized()
	return v1 + (ab * (p - v1).dot(ab))

static func is_other_unit_blocking_path(cur_pos, other_pos, v1, v2, blocking_distance):
	var normal_point = get_normal_point(other_pos, v1, v2)
	var path_distance = (v2 - v1 - cur_pos).length()
	var other_distance_path = (normal_point - v1 - cur_pos).length()
	if other_pos.distance_to(normal_point) > blocking_distance and path_distance * 2 < other_distance_path:
		return false
	return true

static func follow_path(cur_pos, cur_vel, v1, v2, radius, predict_dist, max_force, max_vel):
	var predict = cur_pos + cur_vel.normalized() * predict_dist
	var normal_point = get_normal_point(predict, v1, v2)
	var target = normal_point + (v2 - v1).normalized() * (predict_dist / 2)
	if predict.distance_to(normal_point) > radius:
		return steering(cur_pos, target, cur_vel, max_force, max_vel)
	return Vector2()

static func collision_avoid(cur_pos, cur_vel, obstacle_pos, obstacle_radius, max_force, max_vel):
	var ahead = cur_pos + cur_vel.normalized() * (cur_vel.length() / max_vel)
	if ahead.distance_to(obstacle_pos) > obstacle_radius or (ahead / 2).distance_to(obstacle_pos) > obstacle_radius:
		return Vector2()
	var desired_vel = (ahead - obstacle_pos).normalized() * max_vel
	return ((desired_vel - cur_vel) / max_force).clamped(max_force)

static func collision_slide(cur_pos, cur_vel, obstacle_pos, obstacle_radius, max_force, max_vel):
	var ahead = cur_pos + cur_vel.normalized() * (cur_vel.length() / max_vel)
	if ahead.distance_to(obstacle_pos) > obstacle_radius or (ahead / 2).distance_to(obstacle_pos) > obstacle_radius:
		return Vector2()
	var desired_vel = (ahead - obstacle_pos).normalized().slide(cur_vel) * max_vel
	return ((desired_vel - cur_vel) / max_force).clamped(max_force)

static func steer(cur_pos, target_pos, cur_vel, max_force, max_vel):
	var desired_vel = (target_pos - cur_pos).normalized() * max_vel
	return ((desired_vel - cur_vel) / max_force).clamped(max_force)

static func steer_and_arrive(cur_pos, target_pos, cur_vel, max_force, max_vel, mindist):
	var distance_to_target = target_pos - cur_pos
	var desired_vel = distance_to_target.normalized() * max_vel
	distance_to_target = distance_to_target.length()
	if distance_to_target < mindist:
		desired_vel *= distance_to_target / mindist
	return ((desired_vel - cur_vel) / max_force).clamped(max_force)

static func intercept(cur_pos, target_pos, cur_vel, target_vel, max_force, max_vel, delta):
	return steering(cur_pos + target_vel * delta, target_pos, cur_vel, max_force, max_vel)

static func flee(cur_pos, target_pos, cur_vel, max_force, max_vel, mindist):
	var distance_to_target = target_pos - cur_pos
	if distance_to_target.length() > mindist:
		return Vector2()
	var desired_vel = -distance_to_target.normalized() * max_vel
	return ((desired_vel - cur_vel) / max_force).clamped(max_force)

static func wander(cur_vel, cdist, cradius, max_force):
	var circle_center = cur_vel.normalized() * cdist
	var wander_vector = Vector2(cradius, 0.0).rotated(randf() * 2 * PI)
	return (circle_center + wander_vector).clamped(max_force)

static func separation( cur_pos, other_pos, scaling, mindist ):
	var steering_force = Vector2( 0, 0 )
	var counter = 0
	for other in other_pos:
		var distance = other - cur_pos
		if distance.length() < mindist:
			counter += 1
			steering_force -= distance
	if counter > 0:
		steering_force /= counter
	steering_force *= scaling
	return steering_force

static func flocking(source, targets, separation_scaling, alignment_scaling, cohesion_scaling):
	if !targets:
		return Vector2()
	var cur_pos = source.get_global_position()
	var separation_force = Vector2()
	var separation_counter = 0
	var alignment_vel = Vector2()
	var alignment_counter = 0
	var cohesion_center = cur_pos
	var cohesion_counter = 1
	var other_pos
	for target in targets:
		if target.dead:
			continue
		other_pos = target.get_global_position()
		var distance_vec = other_pos - cur_pos
		var distance = distance_vec.length()
		if distance < 2:
			distance = 2
		separation_force -= distance_vec.normalized() * ( 1 / distance )
		separation_counter += 1
		alignment_vel += target.vel
		alignment_counter += 1
		cohesion_center += other_pos
		cohesion_counter += 1
	if separation_counter > 0:
		separation_force /= separation_counter
	separation_force *= separation_scaling
	var alignment_force = Vector2()
	if alignment_counter > 0:
		alignment_vel /= alignment_counter
		alignment_force += ( alignment_vel - source.vel ) * alignment_scaling
	cohesion_center /= cohesion_counter
	var cohesion_force = ( cohesion_center - cur_pos ) * cohesion_scaling
	return separation_force + alignment_force + cohesion_force