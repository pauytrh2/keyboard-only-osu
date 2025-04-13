class Parser:
    def get_stats(self, text) -> int:
        sections = text.split("\n\n")
        for section in sections:
            if "[Difficulty]" in section:
                lines = section.split("\n")
                for line in lines:
                    if "CircleSize:" in line:
                        self.circle_size = float(line.split(":")[1].strip())
                        if self.HR:
                            self.circle_size *= 1.3
                        if self.EZ:
                            self.circle_size /= 2
                        self.circle_size = int(109 - (9 * self.circle_size))
                    if "ApproachRate:" in line:
                        AR = float(line.split(":")[1].strip())
                        if self.HR:
                            AR = min(10, AR * 1.14)
                        elif self.EZ:
                            AR /= 2

                        if AR < 5:
                            preempt = 1200 + 600 * (5 - AR) / 5
                        elif AR == 5:
                            preempt = 1200
                        else:
                            preempt = 1200 + 750 * (AR - 5) / 5

                        if self.DT:
                            preempt = int(preempt * (2/3))

                        return max(int(preempt), 300)

    def extract_slider_points(self, slider_type, slider_data):
        points = slider_data.split('|')
        extracted_points = [tuple(map(int, point.split(':'))) for point in points[1:] if ':' in point]
        return extracted_points

    def extract_info(self, components) -> tuple:
        x = int(int(components[0]) * 2.25 + 384)
        y = int(int(components[1]) * 2.25 + 126)
        delay = int(components[2])
        object_type = "slider" if len(components) > 6 else "circle"
        slider_points = None

        if object_type == "slider":
            slider_data = components[5]
            slider_type = slider_data.split("|")[0]
            if ":" in slider_data:
                slider_points = self.extract_slider_points(slider_type, slider_data)

        return (x, y, delay, object_type, slider_points)

    def load_circle_info(self) -> list:
        self.circle_removal_delay = self.get_stats(self.mapdata)
        hitobject_lines = self.mapdata.split("[HitObjects]")[1].strip().split("\n")[1:]

        circles_info = [
            self.extract_info(line.split(','))
            for line in hitobject_lines if len(line.split(',')) > 2
        ]

        if not circles_info:
            return []

        initial_delay = circles_info[0][2] + 20

        if self.EZ:
            initial_delay -= self.circle_removal_delay
            initial_delay += 450
            self.circle_removal_delay = 450

        first_line = hitobject_lines[0]
        if first_line.count(",") == 6:
            initial_delay += 70

        # Apply mod transformations
        transformed_info = []
        for x, y, delay, object_type, sliderend in circles_info:
            if self.DT and self.HR:
                new_x, new_y = x, 1116 - y
                new_delay = int(delay / 1.5 - initial_delay / 1.5)
            elif self.DT:
                new_x, new_y = x, y
                new_delay = int(delay / 1.5 - initial_delay / 1.5)
            elif self.HR:
                new_x, new_y = x, 1116 - y
                new_delay = delay - initial_delay
            else:
                new_x, new_y = x, y
                new_delay = delay - initial_delay

            transformed_info.append((new_x, new_y, new_delay, object_type, sliderend))

        return transformed_info