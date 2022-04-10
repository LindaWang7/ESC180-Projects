def initialize():
    global cur_hedons, cur_health
    global cur_time     # int keep track of total duration before reset
    global bored_with_stars
    global tired
    global cur_star_activity, cur_star
    global run_duration     #keep track of total run time before other activities occurs
    global rest_count       #keep track of total rest time

    cur_hedons = 0
    cur_health = 0

    cur_star = 0
    cur_star_activity = None

    bored_with_stars = False

    cur_time = 0
    tired = False
    run_duration = 0
    rest_count=0

def star_can_be_taken(activity):
    """
    check if a star can be taken to gain extra hedons
    :param activity: type of activity either running or textbook
    :return: boolean of if the activity can gain extra hedons
    """
    if not bored_with_stars and cur_star_activity == activity:
        return True
    return False

def perform_activity(activity, duration):
    """
    :param activity: the 3 type of activities
    :param duration: time in min
    :return: no returns
    """
    global cur_health, cur_hedons, cur_time
    global tired
    global cur_star_activity, cur_star
    global run_duration
    global rest_count

    if cur_star_activity!=None:
        cur_time += duration    #update current time by given paramter: duration

    if cur_time >= 120:     #every 2 hours the time and star count reset to calculate bored_with_star
        cur_time = 0        #making the last star value the beginning duration
        cur_star = 0

    # star hedon calculate
    if star_can_be_taken(activity):
        if duration <= 10:
            cur_hedons += duration * 3
        else:
            cur_hedons += 30

    cur_star_activity = None       #make the cur_star_activity invalid to make sure it's used right away

    if activity == 'running':
        rest_count=0    # if there is activity in between rests, rest count does not accumulate
        run_duration += duration
        if tired:
            cur_hedons += (-2) * duration
        else:
            if duration <= 10:
                cur_hedons += 2 * duration
            else:
                cur_hedons += 20 - 2 * (duration - 10)

        # health
        before_duration = run_duration - duration       #the total run time before this duration
        availle_three = 180 - before_duration           #avaiable time that can gain +3 health per min

        if duration <= 180:
            if before_duration < 180:
                if duration < availle_three:
                    cur_health += duration * 3
                else:
                    cur_health += availle_three * 3
                    cur_health += duration - availle_three
            else:
                cur_health += duration
        else:
            if before_duration < 180:
                cur_health += availle_three * 3
                cur_health += duration - availle_three
            else:
                cur_health += duration

        tired = True


    elif activity == 'textbooks':
        rest_count=0    # if there is activity in between rests, rest count does not accumulate
        run_duration = 0
        cur_health += 2 * duration

        if tired:
            cur_hedons += (-2) * duration
        else:
            if duration <= 20:
                cur_hedons += duration
            else:
                cur_hedons += 20 - 1 * (duration - 20)

        tired = True

    elif activity == 'resting':
        run_duration = 0
        rest_count+=duration
        if rest_count >= 120:
            rest_count=0
            tired = False

    else:
        pass            #invalid activity


def get_cur_hedons():
    return cur_hedons


def get_cur_health():
    return cur_health


def offer_star(activity):
    """
    offer a star to the given activity
    :param activity: the 3 types of activities
    :return: no return
    """
    global cur_star_activity, bored_with_stars, cur_star

    cur_star_activity = activity    #reset the current star activity
    cur_star += 1
    if cur_star >= 3:      #if star>=3 in 2 hours(time change calculated in perform_activity)
        bored_with_stars = True


def most_fun_activity_minute():
    """
    consider the current situation and account for hedons
    :return: the activity yields the most hedons
    """
    global cur_star_activity

    if bored_with_stars:
        cur_star_activity = None   #if the user is bored with star treat as no star

    if cur_star_activity == None:
        if tired:
            return "resting"
        else:
            return "running"

    elif cur_star_activity == "running":
        return "running"

    elif cur_star_activity == "textbooks":
        return "textbooks"
    else:
        return "resting"


if __name__ == '__main__':
    initialize()
    perform_activity("textbooks", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 140)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    perform_activity("resting", 100)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("running")
    perform_activity("resting", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    perform_activity("textbooks", 10)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 140)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("resting", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    print(most_fun_activity_minute())
    perform_activity("textbooks", 90)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("resting", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    offer_star("textbooks")
    perform_activity("resting", 20)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 80)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("resting", 100)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("resting", 20)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    perform_activity("running", 140)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    perform_activity("running", 30)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 100)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    perform_activity("running", 110)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    offer_star("running")
    perform_activity("resting", 90)
    print(get_cur_health())
    print(get_cur_hedons())