from manim import * 

class CreatePendulum(Scene):
    def construct(self): 
        upperDot = Dot([0, 2, 0]) 
        lowerDot = Dot([0, -.5, 0])
        lineMoving = Line(upperDot.get_center(), lowerDot.get_center()) 
        oldTheta = ValueTracker(0) 
        newTheta = ValueTracker(0)
        self.add(lineMoving, upperDot)

        def lineUpdater(x): 
            x.rotate((newTheta.get_value() - oldTheta.get_value()), about_point=upperDot.get_center())
            oldTheta.set_value(newTheta.get_value()) 
    
        lineMoving.add_updater(lineUpdater) 

        positions = self.getTheta(10) 

        self.play(newTheta.animate.set_value(positions[0]))
        self.wait()

        maxValues = []
        inBetween = []
        counter = 0
        i = 1 
        while i < len(positions) - 1: 
            while i < len(positions) - 1 and abs(positions[i+1]) < abs(positions[i]):
                i += 1
                counter += 1
            while i < len(positions)-1 and abs(positions[i+1]) > abs(positions[i]): 
                i += 1 
                counter += 1
            maxValues.append(positions[i])
            inBetween.append(counter) 
            counter = 0

        for i in range(len(maxValues)): 
            #either this or smooth as rate function
            self.play(newTheta.animate(run_time=(inBetween[i]*0.01), rate_func=rate_functions.ease_in_out_sine).set_value(maxValues[i]))

    #math: 
    def getTheta_double_dot(self, theta, theta_dot):
        mu = .5 
        return (-mu * theta_dot) - (9.8/2)*np.sin(theta)

    def getTheta(self, t):
        theta =  np.pi / 3 
        theta_dot = 0
        delta_t = 0.01

        positions = [theta]
        for time in np.arange(0, t, delta_t): 
            theta_double_dot = self.getTheta_double_dot(theta, theta_dot)
            theta += theta_dot * delta_t 
            theta_dot += theta_double_dot * delta_t  
            positions.append(theta) 
        return positions
    

    
