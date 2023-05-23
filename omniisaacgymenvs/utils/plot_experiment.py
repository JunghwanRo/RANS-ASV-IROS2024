import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np


def plot_episode_data_virtual(ep_data, save_dir):

    control_history = ep_data['act']
    reward_history = ep_data['rews']
    info_history = ep_data['info']
    state_history = ep_data['obs']
    all_distances = ep_data['all_dist']
    tgrid = np.linspace(0, len(control_history), len(control_history))
    fig_count = 0

    # °°°°°°°°°°°°°°°°°°°°°°°° plot linear speeds in time °°°°°°°°°°°°°°°°°°°°°°°°°
    lin_vels = state_history[:, 2:4]
    # plot linear velocity
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, lin_vels[:, 0], 'r-')
    plt.plot(tgrid, lin_vels[:, 1], 'g-')
    plt.xlabel('Time steps')
    plt.ylabel('Velocity [m/s]')
    plt.legend(['x', 'y'], loc='lower right')
    plt.title('Velocity state history')
    plt.grid()
    plt.savefig(save_dir + '_lin_vel')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot angular speeds in time °°°°°°°°°°°°°°°°°°°°°°°°°
    ang_vel_z = state_history[:, 4:5]
    # plot angular speed (z coordinate)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, ang_vel_z, 'b-')
    plt.xlabel('Time steps')
    plt.ylabel('Angular speed [rad/s]')
    plt.legend(['z'], loc='lower right')
    plt.title('Angular speed state history')
    plt.grid()
    plt.savefig(save_dir + '_ang_vel')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot heading cos, sin °°°°°°°°°°°°°°°°°°°°°°°°°
    headings = state_history[:, :2]
    # plot position (x, y coordinates)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, headings[:, 0], 'r-') # cos
    plt.plot(tgrid, headings[:, 1], 'g-') # sin
    plt.xlabel('Time steps')
    plt.ylabel('Heading')
    plt.legend(['cos(${\\theta}$)', 'sin(${\\theta}$)'], loc='lower right')
    plt.title('Heading state history')
    plt.grid()
    plt.savefig(save_dir + '_heading')


    # °°°°°°°°°°°°°°°°°°°°°°°° plot absolute heading angle °°°°°°°°°°°°°°°°°°°°°°°°°
    headings = state_history[:, :2]
    angles = np.arctan2(headings[:, 0], headings[:, 1])
    angles = np.where(angles < 0, angles + np.pi, angles)
    # plot position (x, y coordinates)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, angles, 'c-')
    plt.xlabel('Time steps')
    plt.ylabel('Angle [rad]')
    plt.legend(['${\\theta}$'], loc='lower right')
    plt.title('Angle state history')
    plt.grid()
    plt.savefig(save_dir + '_angle')
# Compute the angle using numpy.arctan2

    # °°°°°°°°°°°°°°°°°°°°°°°° plot actions in time °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    control_history = np.array(control_history)
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b-', 'g-', 'r-', 'c-']
    for k in range(control_history.shape[1]):
        col = colours[k % control_history.shape[0]]
        plt.step(tgrid, control_history[:, k], col)
    plt.xlabel('Time steps')
    plt.ylabel('Control [N]')
    plt.legend([f'u{k}' for k in range(control_history.shape[1])], loc='lower right')
    plt.title('Thrust control')
    plt.grid()
    plt.savefig(save_dir + '_actions')
    
        # °°°°°°°°°°°°°°°°°°°°°°°° plot actions histogram °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    control_history = np.array(control_history)
    n_bins = len(control_history[0])  
    minor_locator = AutoMinorLocator(2)
    plt.gca().xaxis.set_minor_locator(minor_locator) 
    n, bins, patches = plt.hist(np.sum(control_history, axis=1), bins=len(control_history[0]), edgecolor='white')

    xticks = [(bins[idx+1] + value)/2 for idx, value in enumerate(bins[:-1])]
    ticklabels = [f'T{i+1}' for i in range(n_bins)]
    plt.xticks(xticks, ticklabels)
    plt.yticks([])
    for idx, value in enumerate(n):
        if value > 0:
            plt.text(xticks[idx], value, int(value), ha='center')
    plt.title('Number of thrusts in episode')
    
    plt.savefig(save_dir + '_actions_hist')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot rewards °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, reward_history, 'b-')
    plt.xlabel('Time steps')
    plt.ylabel('Reward')
    plt.legend(['reward'], loc='lower right')
    plt.title('Reward history')
    plt.grid()
    # plt.show()
    plt.savefig(save_dir + '_reward')

    # °°°°°°°°°°°°°°°°°°°°°°°° plot x, y position error over time °°°°°°°°°°°°°°°°°°°°°°°°°
    pos_error = state_history[:, 6:8]
    # plot position (x, y coordinates)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, pos_error[:, 0], 'r-')
    plt.plot(tgrid, pos_error[:, 1], 'g-')
    plt.xlabel('Time steps')
    plt.ylabel('Position [m]')
    plt.legend(['x position', 'y position'], loc='lower right')
    plt.title('Planar position')
    plt.grid()
    plt.savefig(save_dir + '_pos_error')

    # °°°°°°°°°°°°°°°°°°°°°°°° plot distance to target over time °°°°°°°°°°°°°°°°°°°°°°°°°
    pos_error = state_history[:, 6:8]
    # plot position (x, y coordinates)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, np.linalg.norm(np.array([pos_error[:, 0], pos_error[:, 1]]), axis=0), 'c')
    plt.xlabel('Time steps')
    plt.ylabel('Distance [m]')
    plt.legend(['x position', 'y position'], loc='lower right')
    plt.title('Distance to target')
    plt.grid()
    plt.savefig(save_dir + '_dist_to_target')

    # °°°°°°°°°°°°°°°°°°°°°°°° plot meand and std distance °°°°°°°°°°°°°°°°°°°°°°°°°
    fig, ax = plt.subplots()
    ax.plot(tgrid, all_distances.mean(axis=1), alpha=0.5, color='blue', label='mean_dist', linewidth = 4.0)
    ax.fill_between(tgrid, all_distances.mean(axis=1) - all_distances.std(axis=1), all_distances.mean(axis=1) + all_distances.std(axis=1), color='blue', alpha=0.4)
    ax.fill_between(tgrid, all_distances.mean(axis=1) - 2*all_distances.std(axis=1), all_distances.mean(axis=1) + 2*all_distances.std(axis=1), color='blue', alpha=0.2)
    plt.xlabel('Time steps')
    plt.ylabel('Distance [m]')
    plt.legend(['mean', '1-std', '2-std'], loc='best')
    plt.title(f'Mean distance over {all_distances.shape[1]} episodes')
    plt.grid()
    plt.savefig(save_dir + '_mean_dist')


def plot_episode_data_old(ep_data, save_dir):

    control_history = ep_data['act']
    reward_history = ep_data['rews']
    info_history = ep_data['info']
    state_history = ep_data['obs']
    tgrid = np.linspace(0, len(control_history), len(control_history))
    fig_count = 0

    # °°°°°°°°°°°°°°°°°°°°°°°° plot linear speeds in time °°°°°°°°°°°°°°°°°°°°°°°°°
    lin_vels = state_history[:, 12:15]
    # plot linear velocity
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, lin_vels[:, 0], 'r-')
    plt.plot(tgrid, lin_vels[:, 1], 'g-')
    plt.plot(tgrid, lin_vels[:, 2], 'b-')
    plt.xlabel('Time steps')
    plt.ylabel('Velocity [m/s]')
    plt.legend(['x', 'y'], loc='lower right')
    plt.title('Velocity state history')
    plt.grid()
    plt.savefig(save_dir + '_lin_vel')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot angular speeds in time °°°°°°°°°°°°°°°°°°°°°°°°°
    ang_vels = state_history[:, 15:18]
    # plot angular speed (z coordinate)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    #plt.plot(tgrid, ang_vels[:, 0], 'r-')
    #plt.plot(tgrid, ang_vels[:, 1], 'g-')
    plt.plot(tgrid, ang_vels[:, 2], 'b-')
    plt.xlabel('Time steps')
    plt.ylabel('Angular speed [rad/s]')
    plt.legend(['z'], loc='lower right')
    plt.title('Angular speed state history')
    plt.grid()
    plt.savefig(save_dir + '_ang_vel')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot distance to target time °°°°°°°°°°°°°°°°°°°°°°°°°
    positions = state_history[:, :3]
    # plot position (x, y coordinates)
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, positions[:, 0], 'r-')
    plt.plot(tgrid, positions[:, 1], 'g-')
    plt.xlabel('Time steps')
    plt.ylabel('Position [m]')
    plt.legend(['x', 'y'], loc='lower right')
    plt.title('Position state history')
    plt.grid()
    plt.savefig(save_dir + '_pos')

    # °°°°°°°°°°°°°°°°°°°°°°°° plot actions in time °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    control_history = np.array(control_history)
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b-', 'g-', 'r-', 'c-']
    for k in range(control_history.shape[1]):
        col = colours[k % control_history.shape[0]]
        plt.step(tgrid, control_history[:, k], col)
    plt.xlabel('Time steps')
    plt.ylabel('Control [N]')
    plt.legend([f'u{k}' for k in range(control_history.shape[1])], loc='lower right')
    plt.title('Thrust control')
    plt.grid()
    plt.savefig(save_dir + '_actions')
    
        # °°°°°°°°°°°°°°°°°°°°°°°° plot actions histogram °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    control_history = np.array(control_history)
    n_bins = len(control_history[0])  
    minor_locator = AutoMinorLocator(2)
    plt.gca().xaxis.set_minor_locator(minor_locator) 
    n, bins, patches = plt.hist(np.sum(control_history, axis=1), bins=len(control_history[0]), edgecolor='white')

    xticks = [(bins[idx+1] + value)/2 for idx, value in enumerate(bins[:-1])]
    ticklabels = [f'T{i+1}' for i in range(n_bins)]
    plt.xticks(xticks, ticklabels)
    plt.yticks([])
    for idx, value in enumerate(n):
        if value > 0:
            plt.text(xticks[idx], value+5, int(value), ha='center')
    plt.title('Number of thrusts in episode')
    
    plt.savefig(save_dir + '_actions_hist')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot rewards °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    plt.figure(fig_count)
    plt.clf()
    plt.plot(tgrid, reward_history, 'b-')
    plt.xlabel('Time steps')
    plt.ylabel('Reward')
    plt.legend(['reward'], loc='lower right')
    plt.title('Reward history')
    plt.grid()
    # plt.show()
    plt.savefig(save_dir + '_reward')

    # °°°°°°°°°°°°°°°°°°°°°°°° plot dist to target °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    if 'episode' in info_history[0].keys() and ('position_error' and 'heading_error') in info_history[0]['episode'].keys():
        pos_error = np.array([info_history[j]['episode']['position_error'].cpu().numpy() for j in range(len(info_history))])
        head_error = np.array([info_history[j]['episode']['heading_error'].cpu().numpy() for j in range(len(info_history))])
        plt.figure(fig_count)
        plt.clf()

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Time steps')
        ax1.set_ylabel('Position error [m]', color=color)
        ax1.plot(tgrid, pos_error, color=color)
        ax1.grid()
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Heading error [rad]', color=color)  # we already handled the x-label with ax1
        ax2.plot(tgrid, head_error, color=color)
        plt.title('Precision metrics')
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #ax2.grid()
        plt.savefig(save_dir + '_distance_error')
    # °°°°°°°°°°°°°°°°°°°°°°°° plot dist to target rewards °°°°°°°°°°°°°°°°°°°°°°°°°
    fig_count += 1
    if 'episode' in info_history[0].keys() and ('position_reward' and 'heading_reward') in info_history[0]['episode'].keys():
        pos_error = np.array([info_history[j]['episode']['position_reward'].cpu().numpy() for j in range(len(info_history))])
        head_error = np.array([info_history[j]['episode']['heading_reward'].cpu().numpy() for j in range(len(info_history))])
        plt.figure(fig_count)
        plt.clf()

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Time steps')
        ax1.set_ylabel('Position reward', color=color)
        ax1.plot(tgrid, pos_error, color=color)
        ax1.grid()
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('Heading reward', color=color)  # we already handled the x-label with ax1
        ax2.plot(tgrid, head_error, color=color)
        plt.title('Rewards')
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #ax2.grid()
        plt.savefig(save_dir + '_rewards_infos')